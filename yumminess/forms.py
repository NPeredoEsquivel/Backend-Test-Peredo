from django import forms
from .models import Employee, MenuPlate, MenuOption, Menu, Order
from datetime import date


class EmployeeForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=50)
    phone_number = forms.CharField(max_length=20)
    country = forms.CharField(max_length=30)
    username = forms.CharField(max_length=30)
    password = forms.PasswordInput()

    class Meta:
        model = Employee
        exclude = ['enabled', 'created_at', 'user']

    field_order = ['first_name', 'last_name', 'email', 'phone_number', 'country', 'username', 'password']


class MenuPlateForm(forms.ModelForm):
    menu_plate_name = forms.CharField(max_length=30)

    class Meta:
        model = MenuPlate
        exclude = ['created_at']


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

    def clean(self, *args, **kwargs):
        menu_option_entrance_plate = self.cleaned_data.get("menu_option_entrance_plate")
        menu_option_bottom_plate = self.cleaned_data.get("menu_option_bottom_plate")
        menu_option_dessert_plate = self.cleaned_data.get("menu_option_dessert_plate")

        print(menu_option_entrance_plate)
        print(menu_option_bottom_plate)
        print(menu_option_dessert_plate)


class MenuForm(forms.ModelForm):
    menu_name = forms.CharField(max_length=30)
    menu_options = forms.ModelMultipleChoiceField(queryset=MenuOption.objects.all())

    class Meta:
        model = Menu
        exclude = ['uuid', 'created_at']


class OrderForm(forms.ModelForm):
    menu_options = forms.ModelChoiceField(queryset=MenuOption.objects.none())
    order_customization = forms.CharField(max_length=400)

    class Meta:
        model = Order
        exclude = ['created_at']

    def __init__(self, *args, **kwargs):
        super().__init__()
        # Only one menu per day (menu has multiple options)
        menu = Menu.objects.get(created_at=date.today())
        if menu:
            options = MenuOption.objects.filter(menu__id=menu.id)
            self.fields['menu_options'].queryset = options
