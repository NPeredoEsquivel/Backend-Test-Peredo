from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.contrib.auth.models import User
from datetime import date
from .models import Employee, MenuOptionPlate, MenuOption, Menu, Order
from .forms import EmployeeForm, MenuOptionPlateForm, MenuOptionForm, MenuForm, OrderForm, OrderAdminForm


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
        current_user = request.user
        current_date = date.today()

        if current_user.is_superuser:
            orders = Order.objects.filter(created_at__date=current_date).order_by('-created_at')
        else:
            employee = Employee.objects.get(user__id=current_user.id)
            orders = Order.objects.filter(created_at__date=current_date, employee__id=employee.id).order_by(
                '-created_at')

        menus = Menu.objects.filter(created_at=current_date)

        context = {
            'orders': orders,
            'menus': menus
        }

        return render(request, self.template_name, context)


class EmployeeListView(LoginRequiredMixin, ListView):
    login_url = '/yumminess/login'
    model = Employee
    template_name = 'employee/list.html'
    context_object_name = 'employees'

    def get_queryset(self):
        return Employee.objects.all()


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    login_url = '/yumminess/login'
    form_class = EmployeeForm
    template_name = 'employee/create.html'
    success_url = reverse_lazy('yumminess:employee_list')

    def form_valid(self, form):
        employee = form.save(commit=False)
        User.objects.create_user(username=form.cleaned_data['username'],
                                 email=form.cleaned_data['email'],
                                 password=form.cleaned_data['password'])
        employee.user = User.objects.get(username=employee.username)
        employee.save()
        return super().form_valid(form)


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    login_url = '/yumminess/login'
    model = Employee
    template_name = 'employee/detail.html'
    context_object_name = 'yumminess:employee_detail'


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/yumminess/login'
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee/update.html'
    context_object_name = 'employee'

    def get_success_url(self):
        return reverse_lazy('yumminess:employee_detail', kwargs={'pk': self.object.id})


class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    template_name = 'employee/delete.html'
    success_url = reverse_lazy('yumminess:employee_list')

    def delete(self, request, *args, **kwargs):
        employee = self.get_object()
        User.objects.get(id=employee.user_id).delete()
        return HttpResponseRedirect(self.get_success_url())


class MenuOptionPlateListView(LoginRequiredMixin, ListView):
    login_url = '/yumminess/login'
    model = MenuOptionPlate
    template_name = 'menu_option_plate/list.html'
    context_object_name = 'menu_option_plates'

    def get_queryset(self):
        return MenuOptionPlate.objects.all()


class MenuOptionPlateCreateView(LoginRequiredMixin, CreateView):
    login_url = '/yumminess/login'
    form_class = MenuOptionPlateForm
    template_name = 'menu_option_plate/create.html'
    success_url = reverse_lazy('yumminess:menu_option_plate_list')


class MenuOptionPlateDetailView(LoginRequiredMixin, DetailView):
    login_url = '/yumminess/login'
    model = MenuOptionPlate
    template_name = 'menu_option_plate/detail.html'
    context_object_name = 'yumminess:menu_option_plate_detail'


class MenuOptionPlateUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/yumminess/login'
    model = MenuOptionPlate
    form_class = MenuOptionPlateForm
    template_name = 'menu_option_plate/update.html'
    context_object_name = 'menu_option_plate'

    def get_success_url(self):
        return reverse_lazy('yumminess:menu_option_plate_detail', kwargs={'pk': self.object.id})


class MenuOptionPlateDeleteView(LoginRequiredMixin, DeleteView):
    model = MenuOptionPlate
    template_name = 'menu_option_plate/delete.html'
    success_url = reverse_lazy('yumminess:menu_option_plate_list')


class MenuOptionListView(LoginRequiredMixin, ListView):
    login_url = '/yumminess/login'
    model = MenuOption
    template_name = 'menu_option/list.html'
    context_object_name = 'options'

    def get_queryset(self):
        return MenuOption.objects.all().order_by('-created_at')


class MenuOptionCreateView(LoginRequiredMixin, CreateView):
    login_url = '/yumminess/login'
    form_class = MenuOptionForm
    template_name = 'menu_option/create.html'
    success_url = reverse_lazy('yumminess:menu_option_list')


class MenuOptionDetailView(LoginRequiredMixin, DetailView):
    login_url = '/yumminess/login'
    model = MenuOption
    template_name = 'menu_option/detail.html'
    context_object_name = 'yumminess:menu_option_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_option_entrance_plate'] = MenuOptionPlate.objects.filter(
            menu_option_entrance_plate=self.kwargs['pk'])
        context['menu_option_bottom_plate'] = MenuOptionPlate.objects.filter(menu_option_bottom_plate=self.kwargs['pk'])
        context['menu_option_dessert_plate'] = MenuOptionPlate.objects.filter(
            menu_option_dessert_plate=self.kwargs['pk'])

        return context


class MenuOptionUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/yumminess/login'
    model = MenuOption
    form_class = MenuOptionForm
    template_name = 'menu_option/update.html'
    context_object_name = 'menu_option'

    def get_success_url(self):
        return reverse_lazy('yumminess:menu_option_detail', kwargs={'pk': self.object.id})


class MenuOptionDeleteView(LoginRequiredMixin, DeleteView):
    model = MenuOption
    template_name = 'menu_option/delete.html'
    success_url = reverse_lazy('yumminess:menu_option_list')


class MenuListView(LoginRequiredMixin, ListView):
    login_url = '/yumminess/login'
    model = Menu
    template_name = 'menu/list.html'
    context_object_name = 'menus'

    def get_queryset(self):
        today_date = date.today()
        current_user = self.request.user

        if current_user.is_superuser:
            menus = Menu.objects.all().order_by('-created_at')
        else:
            menus = Menu.objects.get(created_at=today_date).order_by('-created_at')

        return menus


class MenuCreateView(LoginRequiredMixin, CreateView):
    login_url = '/yumminess/login'
    form_class = MenuForm
    template_name = 'menu/create.html'
    success_url = reverse_lazy('yumminess:menu_list')

    def form_valid(self, form):
        response = super(MenuCreateView, self).form_valid(form)
        menu_uuid = form.instance.uuid
        form.generate_slack_message(menu_uuid)
        return response


class MenuDetailView(DetailView):
    model = Menu
    template_name = 'menu/detail.html'
    context_object_name = 'yumminess:menu_detail'
    pk_url_kwarg = 'pk'
    uuid_url_kwarg = 'menu_uuid'

    def get_object(self, queryset=None):
        pk_kwarg = self.kwargs.get(self.pk_url_kwarg)
        uuid_kwarg = self.kwargs.get(self.uuid_url_kwarg)

        if pk_kwarg:
            return Menu.objects.get(id=pk_kwarg)

        if uuid_kwarg:
            return Menu.objects.get(uuid=uuid_kwarg)

    def get_context_data(self, **kwargs):
        pk_kwarg = self.kwargs.get(self.pk_url_kwarg)
        uuid_kwarg = self.kwargs.get(self.slug_url_kwarg)

        context = super().get_context_data(**kwargs)

        if pk_kwarg:
            context['menu_options'] = MenuOption.objects.filter(menu__id=self.kwargs['pk'])

            return context
        if uuid_kwarg:
            menu = Menu.objects.get(uuid=uuid_kwarg)
            context['menu_options'] = MenuOption.objects.filter(menu__id=menu.id)

        return context


class MenuUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/yumminess/login'
    model = Menu
    form_class = MenuForm
    template_name = 'menu/update.html'
    context_object_name = 'menu'

    def form_valid(self, form):
        response = super(MenuUpdateView, self).form_valid(form)
        menu_uuid = form.instance.uuid

        form.update_slack_message(menu_uuid)
        return response

    def get_success_url(self):
        return reverse_lazy('yumminess:menu_detail', kwargs={'pk': self.object.id})


class MenuDeleteView(LoginRequiredMixin, DeleteView):
    model = Menu
    template_name = 'menu/delete.html'
    success_url = reverse_lazy('yumminess:menu_list')


class OrderListView(LoginRequiredMixin, ListView):
    login_url = '/yumminess/login'
    model = Order
    template_name = 'order/list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        current_date = date.today()
        current_user = self.request.user
        if current_user.is_superuser:
            orders = Order.objects.filter(created_at__date=current_date).order_by('-created_at')
        else:
            employee = Employee.objects.get(user__id=current_user.id)
            orders = Order.objects.filter(created_at__date=current_date, employee__id=employee.id).order_by(
                '-created_at')

        return orders


class OrderCreateView(LoginRequiredMixin, CreateView):
    login_url = '/yumminess/login'
    template_name = 'order/create.html'
    success_url = reverse_lazy('yumminess:order_list')

    def get_form_kwargs(self):
        today_date = date.today()
        kwargs = super(OrderCreateView, self).get_form_kwargs()

        try:
            menu = Menu.objects.get(created_at=today_date)
        except Menu.DoesNotExist:
            menu = None
        if menu:
            kwargs['menu_options'] = MenuOption.objects.filter(menu__id=menu.id)
        else:
            kwargs['menu_options'] = MenuOption.objects.none()
        current_user = self.request.user
        if not current_user.is_superuser:
            kwargs['employee'] = Employee.objects.filter(user__id=current_user.id)

        return kwargs

    def get_form_class(self):
        current_user = self.request.user
        if current_user.is_superuser:
            return OrderAdminForm
        else:
            return OrderForm

    def form_valid(self, form):
        current_user = self.request.user
        if not current_user.is_superuser:
            order = form.save(commit=False)
            employee = Employee.objects.get(user__id=current_user.id)
            order.employee = employee
            order.save()
        return super().form_valid(form)


class OrderDetailView(LoginRequiredMixin, DetailView):
    login_url = '/yumminess/login'
    model = Order
    template_name = 'order/detail.html'
    context_object_name = 'yumminess:order_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_option_id = self.object.menu_option.id
        context['menu_option'] = MenuOption.objects.filter(id=menu_option_id)
        return context

    def dispatch(self, *args, **kwargs):
        current_user = self.request.user
        if not current_user.is_superuser:
            employee = Employee.objects.get(user__id=current_user.id)
            order = self.get_object()

            if order.employee.id != employee.id:
                raise Http404

        return super(OrderDetailView, self).dispatch(*args, **kwargs)


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/yumminess/login'
    model = Order
    template_name = 'order/update.html'
    context_object_name = 'order'

    def get_form_kwargs(self):
        today_date = date.today()
        kwargs = super(OrderUpdateView, self).get_form_kwargs()

        try:
            menu = Menu.objects.get(created_at=today_date)
        except Menu.DoesNotExist:
            menu = None

        if menu:
            kwargs['menu_options'] = MenuOption.objects.filter(menu__id=menu.id)
        else:
            kwargs['menu_options'] = MenuOption.objects.none()
        current_user = self.request.user
        if not current_user.is_superuser:
            kwargs['employee'] = Employee.objects.filter(user__id=current_user.id)

        return kwargs

    def get_form_class(self):
        current_user = self.request.user
        if current_user.is_superuser:
            return OrderAdminForm
        else:
            return OrderForm

    def get_success_url(self):
        return reverse_lazy('yumminess:order_detail', kwargs={'pk': self.object.id})


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = 'order/delete.html'
    success_url = reverse_lazy('yumminess:order_list')
