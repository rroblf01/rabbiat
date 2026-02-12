from django.contrib import admin
from .models import AIModel, Prompt, MCPServer, OutputResponse
from django.utils.safestring import mark_safe
from handler.utils import get_structure_tool_as_html


class PromptAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "model",
        "text",
        "structure_result",
        "get_structure_tool_structure",
        "created_at",
    )
    readonly_fields = ("get_structure_tool_structure",)
    filter_horizontal = ("mcps",)

    def get_structure_tool_structure(self, obj):
        return get_structure_tool_as_html(obj.id)

    get_structure_tool_structure.short_description = "Structure"


class MCPServerAdmin(admin.ModelAdmin):
    list_display = ("name", "path", "description", "created_at")
    readonly_fields = ("created_at", "get_mcp_file_content")

    def get_mcp_file_content(self, obj):
        try:
            with open(obj.path, "r") as file:
                content = file.read()
            return mark_safe(f"<pre>{content}</pre>")
        except Exception as e:
            return f"Error reading file: {e}"


admin.site.register(AIModel)
admin.site.register(Prompt, PromptAdmin)
admin.site.register(MCPServer, MCPServerAdmin)
admin.site.register(OutputResponse)
