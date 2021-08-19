from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from .models import Employee, MenuPlate, MenuOption, Menu, Order
from .forms import EmployeeForm, MenuPlateForm, MenuOptionForm, MenuForm, OrderForm


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
    form_class = EmployeeForm
    template_name = 'employee/create.html'
    success_url = reverse_lazy('yumminess:employee-list')


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    login_url = '/yumminess/login'
    model = Employee
    template_name = 'employee/detail.html'
    context_object_name = 'yumminess:employee-detail'


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/yumminess/login'
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee/update.html'
    context_object_name = 'employee'

    def get_success_url(self):
        return reverse_lazy('yumminess:employee-detail', kwargs={'pk': self.object.id})


class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    template_name = 'employee/delete.html'
    success_url = reverse_lazy('yumminess:employee-list')


class MenuPlateListView(LoginRequiredMixin, ListView):
    login_url = '/yumminess/login'
    model = MenuPlate
    template_name = 'menu-plate/list.html'

    def get_queryset(self):
        return MenuPlate.objects.all()


class MenuPlateCreateView(LoginRequiredMixin, CreateView):
    login_url = '/yumminess/login'
    form_class = MenuPlateForm
    template_name = 'menu-plate/create.html'
    success_url = reverse_lazy('yumminess:menu-plate-list')


class MenuPlateDetailView(LoginRequiredMixin, DetailView):
    login_url = '/yumminess/login'
    model = MenuPlate
    template_name = 'menu-plate/detail.html'
    context_object_name = 'yumminess:menu-plate-detail'


class MenuPlateUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/yumminess/login'
    model = MenuPlate
    form_class = MenuPlateForm
    template_name = 'menu-plate/update.html'
    context_object_name = 'menu-plate'

    def get_success_url(self):
        return reverse_lazy('yumminess:menu-plate-detail', kwargs={'pk': self.object.id})


class MenuPlateDeleteView(LoginRequiredMixin, DeleteView):
    model = MenuPlate
    template_name = 'menu-plate/delete.html'
    success_url = reverse_lazy('yumminess:menu-plate-list')


class MenuOptionListView(LoginRequiredMixin, ListView):
    login_url = '/yumminess/login'
    model = MenuOption
    template_name = 'menu-option/list.html'

    def get_queryset(self):
        return MenuOption.objects.all()


class MenuOptionCreateView(LoginRequiredMixin, CreateView):
    login_url = '/yumminess/login'
    form_class = MenuOptionForm
    template_name = 'menu-option/create.html'
    success_url = reverse_lazy('yumminess:menu-option-list')


class MenuOptionDetailView(LoginRequiredMixin, DetailView):
    login_url = '/yumminess/login'
    model = MenuOption
    template_name = 'menu-option/detail.html'
    context_object_name = 'yumminess:menu-option-detail'


class MenuOptionUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/yumminess/login'
    model = MenuOption
    form_class = MenuOptionForm
    template_name = 'menu-option/update.html'
    context_object_name = 'menu-option'

    def get_success_url(self):
        return reverse_lazy('yumminess:menu-option-detail', kwargs={'pk': self.object.id})


class MenuOptionDeleteView(LoginRequiredMixin, DeleteView):
    model = MenuOption
    template_name = 'menu-option/delete.html'
    success_url = reverse_lazy('yumminess:menu-option-list')


class MenuListView(LoginRequiredMixin, ListView):
    login_url = '/yumminess/login'
    model = Menu
    template_name = 'menu/list.html'

    def get_queryset(self):
        return Menu.objects.all()


class MenuCreateView(LoginRequiredMixin, CreateView):
    login_url = '/yumminess/login'
    form_class = MenuForm
    template_name = 'menu/create.html'
    success_url = reverse_lazy('yumminess:menu-list')


class MenuDetailView(LoginRequiredMixin, DetailView):
    login_url = '/yumminess/login'
    model = Menu
    template_name = 'menu/detail.html'
    context_object_name = 'yumminess:menu-detail'


class MenuUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/yumminess/login'
    model = Menu
    form_class = MenuForm
    template_name = 'menu/update.html'
    context_object_name = 'menu'

    def get_success_url(self):
        return reverse_lazy('yumminess:menu-detail', kwargs={'pk': self.object.id})


class MenuDeleteView(LoginRequiredMixin, DeleteView):
    model = Menu
    template_name = 'menu/delete.html'
    success_url = reverse_lazy('yumminess:menu-list')


class OrderListView(LoginRequiredMixin, ListView):
    login_url = '/yumminess/login'
    model = Order
    template_name = 'order/list.html'

    def get_queryset(self):
        return Order.objects.all()


class OrderCreateView(LoginRequiredMixin, CreateView):
    login_url = '/yumminess/login'
    form_class = OrderForm
    template_name = 'order/create.html'
    success_url = reverse_lazy('yumminess:order-list')


class OrderDetailView(LoginRequiredMixin, DetailView):
    login_url = '/yumminess/login'
    model = Order
    template_name = 'order/detail.html'
    context_object_name = 'yumminess:order-detail'


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/yumminess/login'
    model = Order
    form_class = OrderForm
    template_name = 'order/update.html'
    context_object_name = 'order'

    def get_success_url(self):
        return reverse_lazy('yumminess:order-detail', kwargs={'pk': self.object.id})


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = 'order/delete.html'
    success_url = reverse_lazy('yumminess:order-list')
