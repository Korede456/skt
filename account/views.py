from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import CustomUserLoginForm
from django.shortcuts import render
from django.contrib.auth.views import LogoutView
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.shortcuts import redirect
from .forms import CustomUserRegistrationForm


class CustomUserRegistrationView(View):
    def get(self, request):
        form = CustomUserRegistrationForm()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New user registered successfully")
            return redirect('account:login')
        return render(request, 'account/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'account/login.html'
    authentication_form = CustomUserLoginForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_invalid(self, form):
        # Add custom error handling here
        response = super().form_invalid(form)
        form.add_error(None, "Invalid username or password. Please try again.")
        return response

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('account:login')
    @method_decorator(require_POST, name='dispatch')
    def post(self, request, *args, **kwargs):
        messages.success(request, "You have been logged out successfully.")
        return super().post(request, *args, **kwargs)