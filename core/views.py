from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .models import Ticket
from .forms import RegisterForm, TicketForm, FeedbackForm


# Create your views here.
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "auth.html"
    success_url = reverse_lazy("login")
    extra_context = {
        "title": "Регистрация",
        "button_text": "Создать пользователя",
        "is_registration": True,
    }


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = "tickets.html"
    context_object_name = "tickets"

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user).order_by("-created_at")


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = "form.html"
    success_url = reverse_lazy("home")
    extra_context = {
        "title": "Новое обращение",
        "button_text": "Отправить",
    }

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@login_required
def feedback_create(request, pk):
    ticket = get_object_or_404(
        Ticket,
        pk=pk,
        user=request.user,
        status=Ticket.Status.CLOSED,
        feedback__isnull=True,
    )

    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.ticket = ticket
            feedback.save()
            return redirect("home")
    else:
        form = FeedbackForm()

    return render(
        request,
        "form.html",
        {
            "form": form,
            "title": "Оставить отзыв",
            "button_text": "Отправить отзыв",
        },
    )
