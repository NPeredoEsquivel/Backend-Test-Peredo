from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from .models import Employee


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


class EmployeeListView(LoginRequiredMixin, ListView):
    login_url = '/yumminess/login'
    model = Employee
    template_name = 'employee/list.html'

    def get_queryset(self):
        return Employee.objects.all()


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    login_url = '/yumminess/login'
    model = Employee
    template_name = 'employee/create.html'
    fields = ('country', 'email', 'first_name', 'last_name', 'password', 'phone_number', 'username')
    success_url = reverse_lazy('yumminess:employee-list')


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    login_url = '/yumminess/login'
    model = Employee
    template_name = 'employee/detail.html'
    context_object_name = 'yumminess:employee-detail'


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/yumminess/login'
    model = Employee
    template_name = 'employee/update.html'
    context_object_name = 'employee'
    fields = ('country', 'email', 'first_name', 'last_name', 'password', 'phone_number', 'username')

    def get_success_url(self):
        return reverse_lazy('yumminess:employee-list', kwargs={'pk': self.object.id})


class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    template_name = 'employee/delete.html'
    success_url = reverse_lazy('yumminess:employee-list')