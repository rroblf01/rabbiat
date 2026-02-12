from django.db import models
from django.conf import settings
from asgiref.sync import sync_to_async
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai.providers.openai import OpenAIProvider
from handler.utils import (
    get_structure_tool_classes,
    get_structure_tool_class,
    get_mcp_files,
)


class MCPServer(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(
        max_length=255, choices=[(file, file) for file in get_mcp_files()]
    )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "MCP Server"
        verbose_name_plural = "MCP Servers"
        unique_together = ("name", "path")


class AIModel(models.Model):
    FAMILIES = (("openai", "OpenAI"), ("ollama", "Ollama"))
    name = models.CharField(max_length=100)
    description = models.TextField()
    family = models.CharField(max_length=50, default="ollama")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_provider(self):
        providers = {
            "ollama": OllamaProvider(base_url=settings.PROVIDER_AI_URL),
            "openai": OpenAIProvider(api_key=settings.OPENAI_API_KEY),
        }

        if provider := providers.get(self.family):
            return provider

        raise NotImplementedError(
            f"Provider for family '{self.family}' is not implemented."
        )

    async def get_ai_model(self):
        if self.family != "ollama":
            raise NotImplementedError("OpenAI models are not implemented yet.")

        return OpenAIChatModel(
            model_name=self.name,
            provider=OllamaProvider(base_url=settings.PROVIDER_AI_URL),
        )

    def __str__(self):
        return self.name


class Prompt(models.Model):
    name = models.CharField(max_length=100)
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE, related_name="prompts")
    text = models.TextField()
    structure_result = models.CharField(
        max_length=255,
        choices=[(cls, cls) for cls in get_structure_tool_classes()],
        null=True,
        blank=True,
    )
    mcps = models.ManyToManyField(MCPServer, blank=True, related_name="prompts")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prompt for {self.model.name}"

    async def get_mcp_servers(self) -> list[MCPServerStdio] | None:
        if await self.mcps.all().aexists():
            return [
                MCPServerStdio("python", args=[mcp.path], timeout=10)
                async for mcp in self.mcps.all()
            ]
        return None

    async def get_agent(self):
        model = await sync_to_async(lambda: self.model)()
        model_ai = await model.get_ai_model()

        toolsets = await self.get_mcp_servers()
        data = {
            "model": model_ai,
            "toolsets": toolsets,
            "retries": 3,
        }

        if self.structure_result:
            data["output_type"] = get_structure_tool_class(self.structure_result)

        return Agent(**data)

    async def execute(self, additional_input: str = ""):
        agent = await self.get_agent()
        response = await agent.run(
            (self.text + f"\n\nInformación extra: {additional_input}")
            if additional_input
            else self.text
        )
        output = (
            response.output
            if isinstance(response.output, str)
            else response.output.model_dump()
        )
        await OutputResponse.objects.acreate(
            prompt=self, output=output, usage=response.usage().__dict__
        )
        return response


class OutputResponse(models.Model):
    prompt = models.ForeignKey(
        Prompt, on_delete=models.CASCADE, related_name="responses"
    )
    output = models.TextField()
    usage = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response for {self.prompt}"
