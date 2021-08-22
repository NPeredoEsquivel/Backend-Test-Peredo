from django import forms
from .models import Employee, MenuOptionPlate, MenuOption, Menu, Order, SlackMessage
from datetime import date, datetime
from django.contrib.auth.models import User
from django.conf import settings

project_url = settings.BASE_URL


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


class MenuOptionPlateForm(forms.ModelForm):
    menu_option_plate_name = forms.CharField(max_length=30)

    class Meta:
        model = MenuOptionPlate
        exclude = ['created_at']

    def clean_menu_option_plate_name(self):
        menu_option_plate_name_form_data = self.cleaned_data['menu_option_plate_name']
        if MenuOptionPlate.objects.exclude(pk=self.instance.pk).filter(
                menu_option_plate_name=menu_option_plate_name_form_data).exists():
            raise forms.ValidationError('The menu plate\'s %s already exists' % menu_option_plate_name_form_data)
        return menu_option_plate_name_form_data


class MenuOptionForm(forms.ModelForm):
    # e_plate = entrance_plate (variable name changed for pep8 paragraph length)
    # b_plate = bottom_plate (variable name changed for pep8 paragraph length)
    # d_plate = bottom_plate (variable name changed for pep8 paragraph length)
    e_plate = 1
    b_plate = 2
    d_plate = 3

    menu_option_name = forms.CharField(max_length=30)
    menu_option_entrance_plate = \
        forms.ModelChoiceField(queryset=MenuOptionPlate.objects.filter(menu_option_plate_type=e_plate))
    menu_option_bottom_plate = \
        forms.ModelChoiceField(queryset=MenuOptionPlate.objects.filter(menu_option_plate_type=b_plate))
    menu_option_dessert_plate = \
        forms.ModelChoiceField(queryset=MenuOptionPlate.objects.filter(menu_option_plate_type=d_plate))

    class Meta:
        model = MenuOption
        exclude = ['created_at']

    def clean_menu_option_name(self):
        menu_option_name_form_data = self.cleaned_data['menu_option_name']

        if MenuOption.objects.exclude(pk=self.instance.pk).filter(menu_option_name=menu_option_name_form_data).exists():
            raise forms.ValidationError('The menu option with name %s already exists' % menu_option_name_form_data)
        return menu_option_name_form_data

    def clean(self):
        menu_option_entrance_plate_form_data = self.cleaned_data.get("menu_option_entrance_plate")
        menu_option_bottom_plate_form_data = self.cleaned_data.get("menu_option_bottom_plate")
        menu_option_dessert_plate_form_data = self.cleaned_data.get("menu_option_dessert_plate")

        if MenuOption.objects.exclude(pk=self.instance.pk).filter(
                menu_option_entrance_plate=menu_option_entrance_plate_form_data,
                menu_option_bottom_plate=menu_option_bottom_plate_form_data,
                menu_option_dessert_plate=menu_option_dessert_plate_form_data).exists():
            raise forms.ValidationError('There\'s an option with the same plates you\'ve selected')


def generate_message(*args):
    menu_uuid = args[0]
    created_at = args[1]
    options = args[2]
    print(created_at)
    print(options)

    slack_message = "Hello!\n" \
                    "I share with you today\'s menu :)\n"

    url = project_url + 'yumminess/menu/' + str(menu_uuid)
    option_index = 1
    for option in options:
        menu_option = "Option " + str(option_index) + ": (" + str(option.menu_option_name) + ") " + str(
            option.menu_option_entrance_plate)
        if option.menu_option_bottom_plate:
            menu_option += ", " + str(option.menu_option_bottom_plate)
        menu_option += ", " + str(option.menu_option_dessert_plate) + "."
        slack_message += menu_option + """ \n"""
        option_index += 1

    slack_message += """In the next url you can check the menu!\n""" + str(url)

    SlackMessage.objects.create(created_at=created_at,
                                message_text=slack_message)


class MenuForm(forms.ModelForm):
    menu_name = forms.CharField(max_length=30)
    menu_options = forms.ModelMultipleChoiceField(queryset=MenuOption.objects.all())
    created_at = forms.DateField(widget=DateInput())

    class Meta:
        model = Menu
        exclude = ['uuid']

    def generate_slack_message(self, *args):
        menu_uuid = args[0]
        created_at = self.cleaned_data['created_at']
        options = self.cleaned_data['menu_options']

        generate_message(menu_uuid, created_at, options)

    def update_slack_message(self, *args):
        menu_uuid = args[0]
        created_at = self.cleaned_data['created_at']
        options = self.cleaned_data['menu_options']

        SlackMessage.objects.get(created_at=created_at).delete()

        generate_message(menu_uuid, created_at, options)

    def clean_menu_name(self):
        menu_name_form_data = self.cleaned_data['menu_name']

        if Menu.objects.exclude(pk=self.instance.pk).filter(menu_name=menu_name_form_data).exists():
            raise forms.ValidationError('The menu\'s name %s already exists' % menu_name_form_data)

        return menu_name_form_data

    def clean_created_at(self):
        created_at_form_data = self.cleaned_data.get('created_at')
        today_date = date.today()

        menu_already_exists_for_today = Menu.objects.exclude(pk=self.instance.pk).filter(
            created_at=created_at_form_data)
        if menu_already_exists_for_today:
            raise forms.ValidationError("Only one menu must be created for a particular day")
        if created_at_form_data < today_date:
            raise forms.ValidationError("The date must be higher than today\'s date")

        return created_at_form_data


class OrderForm(forms.ModelForm):
    menu_option = forms.ModelChoiceField(queryset=MenuOption.objects.all())
    order_customization = forms.CharField(required=False, max_length=400)

    class Meta:
        model = Order
        exclude = ['created_at']

    def __init__(self, *args, **kwargs):
        menu_options = kwargs.pop('menu_options')
        employee = kwargs.pop('employee')
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['employee'].queryset = employee
        self.fields['menu_option'].queryset = menu_options

    def clean(self):
        created_at_backend_value = datetime.now()
        created_at_backend_value_date = date.today()
        created_at_limit = datetime.now()

        date_threshold = created_at_limit.replace(hour=11, minute=0, second=0, microsecond=0)

        employee_id = self.cleaned_data['employee']
        order_existence = Order.objects.exclude(pk=self.instance.pk).get(created_at__date=created_at_backend_value_date,
                                                                         employee_id=employee_id)
        if order_existence:
            raise forms.ValidationError("There\'s already an order for today.")

        if created_at_backend_value > date_threshold:
            raise forms.ValidationError("You can no longer create your Order. The deadline is set for 11:00 CLT")


class OrderAdminForm(forms.ModelForm):
    menu_option = forms.ModelChoiceField(queryset=MenuOption.objects.all())
    order_customization = forms.CharField(required=False, max_length=400)
    employee = forms.ModelChoiceField(queryset=Employee.objects.all())

    class Meta:
        model = Order
        exclude = ['created_at']

    def __init__(self, *args, **kwargs):
        menu_options = kwargs.pop('menu_options')
        super(OrderAdminForm, self).__init__(*args, **kwargs)
        self.fields['menu_option'].queryset = menu_options

    def clean(self):
        created_at_backend_value = date.today()

        employee_id = self.cleaned_data['employee']
        order_existence = Order.objects.exclude(pk=self.instance.pk).filter(created_at__date=created_at_backend_value,
                                                                            employee_id=employee_id)
        if order_existence:
            raise forms.ValidationError("There\'s already an order for today.")
