from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if self.request.method == "POST":
            username = self.request.POST.get('username')
            password = self.request.POST.get('password')

            user = authenticate(self.request, username=username, password=password)

            if user is not None:
                login(self.request, user)
                return redirect(reverse('yumminess:dashboard'))
            else:
                messages.error(request, "Usuario o contraseña incorrecto")
                return render(request, self.template_name)


class LogoutView(View):
    template_name = 'login.html'

    def get(self, request):
        logout(request)
        return redirect(reverse('yumminess:login'))


class Dashboard(LoginRequiredMixin, View):
    login_url = '/yumminess/login'

    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)
