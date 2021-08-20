from django import forms
from .models import Employee, MenuPlate, MenuOption, Menu, Order
from datetime import date, datetime
from django.contrib.auth.models import User


class DateInput(forms.DateInput):
    input_type = 'date'


class EmployeeForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=50, widget=forms.EmailInput())
    phone_number = forms.CharField(max_length=20)
    country = forms.CharField(max_length=30)
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Employee
        exclude = ['enabled', 'created_at', 'user']

    field_order = ['first_name', 'last_name', 'email', 'phone_number', 'country', 'username', 'password']

    def clean_username(self):
        username_form_data = self.cleaned_data['username']

        if User.objects.filter(username=username_form_data).exists():
            raise forms.ValidationError('The username %s already exists' % username_form_data)
        return username_form_data


class MenuPlateForm(forms.ModelForm):
    menu_plate_name = forms.CharField(max_length=30)

    class Meta:
        model = MenuPlate
        exclude = ['created_at']

    def clean_menu_plate_name(self):
        menu_plate_name_form_data = self.cleaned_data['menu_plate_name']

        if MenuPlate.objects.filter(menu_plate_name=menu_plate_name_form_data).exists():
            raise forms.ValidationError('The menu plate\'s %s already exists' % menu_plate_name_form_data)
        return menu_plate_name_form_data


class MenuOptionForm(forms.ModelForm):
    # e_plate = entrance_plate (variable name changed for pep8 paragraph length)
    # b_plate = bottom_plate (variable name changed for pep8 paragraph length)
    # d_plate = bottom_plate (variable name changed for pep8 paragraph length)
    e_plate = 1
    b_plate = 2
    d_plate = 3

    menu_option_name = forms.CharField(max_length=30)
    menu_option_entrance_plate = forms.ModelChoiceField(queryset=MenuPlate.objects.filter(menu_plate_type=e_plate))
    menu_option_bottom_plate = forms.ModelChoiceField(queryset=MenuPlate.objects.filter(menu_plate_type=b_plate))
    menu_option_dessert_plate = forms.ModelChoiceField(queryset=MenuPlate.objects.filter(menu_plate_type=d_plate))

    class Meta:
        model = MenuOption
        exclude = ['created_at']

    def clean_menu_option_name(self):
        menu_option_name_form_data = self.cleaned_data['menu_option_name']

        if MenuOption.objects.filter(menu_option_name=menu_option_name_form_data).exists():
            raise forms.ValidationError('The menu option with name %s already exists' % menu_option_name_form_data)
        return menu_option_name_form_data

    def clean(self):
        menu_option_entrance_plate_form_data = self.cleaned_data.get("menu_option_entrance_plate")
        menu_option_bottom_plate_form_data = self.cleaned_data.get("menu_option_bottom_plate")
        menu_option_dessert_plate_form_data = self.cleaned_data.get("menu_option_dessert_plate")

        if MenuOption.objects.filter(menu_option_entrance_plate=menu_option_entrance_plate_form_data,
                                     menu_option_bottom_plate=menu_option_bottom_plate_form_data,
                                     menu_option_dessert_plate=menu_option_dessert_plate_form_data).exists():
            raise forms.ValidationError('There\'s an option with the same plates you\'ve selected')


class MenuForm(forms.ModelForm):
    menu_name = forms.CharField(max_length=30)
    menu_options = forms.ModelMultipleChoiceField(queryset=MenuOption.objects.all())
    created_at = forms.DateField(required=True, widget=DateInput())

    class Meta:
        model = Menu
        exclude = ['uuid']

    def clean_menu_name(self):
        menu_name_form_data = self.cleaned_data['menu_name']

        if Menu.objects.filter(menu_name=menu_name_form_data).exists():
            raise forms.ValidationError('The menu\'s name %s already exists' % menu_name_form_data)
        return menu_name_form_data

    def clean_date_created(self):
        created_at_form_data = self.cleaned_data.get('created_at')
        today_date = date.today()

        menu_already_exists_for_today = Menu.objects.filter(created_at=created_at_form_data)

        if menu_already_exists_for_today:
            raise forms.ValidationError("Only one menu must be created for a particular day")
        if created_at_form_data < today_date:
            raise forms.ValidationError("The date must be higher than today\'s date")


class OrderForm(forms.ModelForm):
    menu_options = forms.ModelChoiceField(queryset=MenuOption.objects.all())
    order_customization = forms.CharField(max_length=400)

    class Meta:
        model = Order
        exclude = ['created_at']

    def __init__(self, *args, **kwargs):
        menu_options = kwargs.pop('menu_options')
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['menu_options'].queryset = menu_options

    def clean(self):
        created_at_backend_value = datetime.now()
        created_at_limit = datetime.now()

        date_threshold = created_at_limit.replace(hour=11, minute=0, second=0, microsecond=0)
        if created_at_backend_value > date_threshold:
            raise forms.ValidationError("You can no longer create your Order. The deadline is set for 11:00 CLT")
