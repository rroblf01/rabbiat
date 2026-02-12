from django.urls import path
from . import views

urlpatterns = [
    path("", views.PromptInterfaceView.as_view(), name="prompt_list"),
]
