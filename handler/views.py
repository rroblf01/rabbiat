from django.views.generic import ListView
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Prompt
import json
from django.contrib.auth.views import LoginView, LogoutView
from asgiref.sync import sync_to_async


class UserLoginView(LoginView):
    template_name = "login.html"

    def get_success_url(self):
        return reverse("prompt_list")


class UserLogoutView(LogoutView):
    next_page = "login"


class PromptInterfaceView(ListView):
    model = Prompt
    template_name = "index.html"
    context_object_name = "prompts"

    async def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not await sync_to_async(lambda: user.is_authenticated)():
            return HttpResponseRedirect("/login/")
        return await super().dispatch(request, *args, **kwargs)

    async def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    async def post(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
            prompt_id = body.get("prompt_id")
            additional_input = body.get("additional_input", "")

            prompt = await Prompt.objects.aget(id=prompt_id)

            result = await prompt.execute(additional_input=additional_input)

            data = (
                result.output
                if isinstance(result.output, str)
                else result.output.model_dump()
            )
            return JsonResponse({"result": data})

        except Prompt.DoesNotExist:
            return JsonResponse({"error": "Prompt no encontrado."}, status=404)
        except Exception as e:
            print(f"Error detectado: {e}")
            return JsonResponse({"error": str(e)}, status=500)
