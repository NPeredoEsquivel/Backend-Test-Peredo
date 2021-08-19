from django import forms

from .models import Employee, MenuPlate, MenuOption, Menu, Order


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['enabled', 'created_at']


class MenuPlateForm(forms.ModelForm):
    class Meta:
        model = MenuPlate
        exclude = ['created_at']


class MenuOptionForm(forms.ModelForm):

    class Meta:
        model = MenuOption
        exclude = ['created_at']


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        exclude = ['uuid', 'created_at']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['created_at']
