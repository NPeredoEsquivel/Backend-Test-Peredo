from django.db import models
from django.contrib.auth.models import User
import uuid


class Employee(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE, default=None)
    country = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30, null=False, default=None)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class SlackMessage(models.Model):
    created_at = models.DateField(auto_now_add=False)
    message_text = models.CharField(max_length=500)
    sent = models.BooleanField(default=False)


class MenuOptionPlate(models.Model):
    MENU_PLATE_TYPES = (
        (1, 'Entrance plate'),
        (2, 'Bottom plate'),
        (3, 'Dessert plate')
    )

    menu_option_plate_name = models.CharField(max_length=30)
    menu_option_plate_type = models.IntegerField(choices=MENU_PLATE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.menu_option_plate_name)


class MenuOption(models.Model):
    menu_option_name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    menu_option_entrance_plate = models.ForeignKey(MenuOptionPlate, related_name='menu_option_entrance_plate',
                                                   limit_choices_to={'menu_option_plate_type': 1},
                                                   on_delete=models.SET_NULL,
                                                   null=True)
    menu_option_bottom_plate = models.ForeignKey(MenuOptionPlate, related_name='menu_option_bottom_plate',
                                                 limit_choices_to={'menu_option_plate_type': 2},
                                                 on_delete=models.SET_NULL,
                                                 null=True)
    menu_option_dessert_plate = models.ForeignKey(MenuOptionPlate, related_name='menu_option_dessert_plate',
                                                  limit_choices_to={'menu_option_plate_type': 3},
                                                  on_delete=models.SET_NULL,
                                                  null=True)

    def __str__(self):
        return str(self.menu_option_name)


class Menu(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4())
    menu_name = models.CharField(max_length=30)
    created_at = models.DateField(auto_now_add=False)
    menu_options = models.ManyToManyField(MenuOption)

    def __str__(self):
        return str(self.menu_name)


class Order(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    menu_option = models.ForeignKey(MenuOption, on_delete=models.SET_NULL, null=True)
    order_customization = models.CharField(max_length=400, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
