from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from .views import (
    RegisterView,
    TicketListView,
    TicketCreateView,
    feedback_create,
)
from .forms import LoginForm

urlpatterns = [
    path("", TicketListView.as_view(), name="home"),
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "login/",
        LoginView.as_view(
            template_name="auth.html",
            authentication_form=LoginForm,
            extra_context={
                "title": "Авторизация",
                "button_text": "Войти",
            },
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("tickets/create/", TicketCreateView.as_view(), name="ticket_create"),
    path("tickets/<int:pk>/feedback/", feedback_create, name="feedback_create"),
]
