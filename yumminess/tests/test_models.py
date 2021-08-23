import pytz
from django.test import TestCase
from yumminess import forms
from django.contrib.auth.models import User
from ..models import MenuOptionPlate, Order, Employee, MenuOption, Menu, SlackMessage
from ..tasks import send_slack_message_menu

from datetime import date, datetime, timedelta


class TestForms(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'tester',
            'password': 'secret'}
        self.user_test = User.objects.create_user(**self.credentials)
        self.employee = Employee.objects.create(
            user=self.user_test,
            username="tester",
            first_name="tester",
            last_name="secret",
            password="secret"
        )

        self.menu_option_starter_plate_one = MenuOptionPlate.objects.create(
            menu_option_plate_name='Spring rolls',
            menu_option_plate_type=1
        )
        self.menu_option_bottom_plate_one = MenuOptionPlate.objects.create(
            menu_option_plate_name='Grilled salmon with dill sauce',
            menu_option_plate_type=2
        )
        self.menu_option_dessert_plate_one = MenuOptionPlate.objects.create(
            menu_option_plate_name='Apple pie with cream',
            menu_option_plate_type=3
        )

        self.menu_option_starter_plate_two = MenuOptionPlate.objects.create(
            menu_option_plate_name='French onion soup',
            menu_option_plate_type=1
        )
        self.menu_option_bottom_plate_two = MenuOptionPlate.objects.create(
            menu_option_plate_name='Roast beef with vegetables',
            menu_option_plate_type=2
        )
        self.menu_option_dessert_plate_two = MenuOptionPlate.objects.create(
            menu_option_plate_name='Lemon meringue pie',
            menu_option_plate_type=3
        )
        self.menu_option_dessert_plate_three = MenuOptionPlate.objects.create(
            menu_option_plate_name='Fruit salad',
            menu_option_plate_type=3
        )
        self.menu_option_dessert_plate_four = MenuOptionPlate.objects.create(
            menu_option_plate_name='Vanilla ice cream',
            menu_option_plate_type=3
        )

        self.option_one = MenuOption.objects.create(
            menu_option_name='Option 1',
            menu_option_entrance_plate=self.menu_option_starter_plate_one,
            menu_option_bottom_plate=self.menu_option_bottom_plate_one,
            menu_option_dessert_plate=self.menu_option_dessert_plate_one
        )
        self.option_two = MenuOption.objects.create(
            menu_option_name='Option 2',
            menu_option_entrance_plate=self.menu_option_starter_plate_two,
            menu_option_bottom_plate=self.menu_option_bottom_plate_two,
            menu_option_dessert_plate=self.menu_option_dessert_plate_two
        )

        self.option_three = MenuOption.objects.create(
            menu_option_name='Option 3',
            menu_option_entrance_plate=self.menu_option_starter_plate_one,
            menu_option_bottom_plate=self.menu_option_bottom_plate_two,
            menu_option_dessert_plate=self.menu_option_dessert_plate_one
        )

        current_date = date.today() + timedelta(1)
        self.menu_one = Menu.objects.create(
            menu_name='First menu',
            created_at=current_date
        )
        self.menu_one.menu_options.set([self.option_one, self.option_two])

        current_date = date.today() + timedelta(2)
        self.menu_two = Menu.objects.create(
            menu_name='Second menu',
            created_at=current_date
        )
        self.menu_two.menu_options.set([self.option_three, self.option_two])

    # Testing menu option plate form with validated data.
    def test_menu_option_plate_form_data(self):
        form = forms.MenuOptionPlateForm(data={
            'menu_option_plate_name': 'Salmon with salad',
            'menu_option_plate_type': 1
        })

        self.assertTrue(form.is_valid())

    # Testing menu option plate form with existing data
    def test__menu_option_plate_form_data_existing_name(self):
        form = forms.MenuOptionPlateForm(data={
            'menu_option_plate_name': 'Spring rolls',
            'menu_option_plate_type': 1,
        })

        self.assertFalse(form.is_valid())

    # Testing menu option plate form with no data
    def test__menu_option_plate_form_no_data(self):
        form = forms.MenuOptionPlateForm(data={
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    # Testing menu option plate form with few data
    def test_menu_option_plate_form_less_data(self):
        form = forms.MenuOptionPlateForm(data={
            'menu_option_plate_name': 'Spring rolls new version',
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    # Testing menu option with data persisted in database.
    def test_menu_option_form_data_existing_plates(self):
        form = forms.MenuOptionForm(data={
            'menu_option_plate_name': 'Option new same plates',
            'menu_option_entrance_plate': self.menu_option_starter_plate_one,
            'menu_option_bottom_plate': self.menu_option_bottom_plate_one,
            'menu_option_dessert_plate': self.menu_option_dessert_plate_one
        })
        self.assertFalse(form.is_valid())

    # Testing menu option with different plates
    def test_menu_option_form_data_correct(self):
        form = forms.MenuOptionForm(data={
            'menu_option_name': 'Option new',
            'menu_option_entrance_plate': self.menu_option_starter_plate_one,
            'menu_option_bottom_plate': self.menu_option_bottom_plate_one,
            'menu_option_dessert_plate': self.menu_option_dessert_plate_three
        })
        self.assertTrue(form.is_valid())

    # Testing the menu option with existing name
    def test_option_form_data_correct_but_same_name(self):
        form = forms.MenuOptionForm(data={
            'menu_option_name': 'Option 1',
            'menu_option_entrance_plate': self.menu_option_starter_plate_one,
            'menu_option_bottom_plate': self.menu_option_bottom_plate_one,
            'menu_option_dessert_plate': self.menu_option_dessert_plate_four
        })
        self.assertFalse(form.is_valid())

    # Testing the option form with no data, expected four violations for the fields in the form.
    def test_option_form_no_data(self):
        form = forms.MenuOptionForm(data={
        })

        # We have two validations, the name and plate_type, so if len of errors are two, it's ok
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    # Testing employee form with valid data
    def test_employee_form_correct_data(self):
        form = forms.EmployeeForm(data={
            'user': self.user_test,
            'first_name': 'User test',
            'last_name': 'Last name test',
            'username': 'username_1',
            'email': 'email@test.com',
            'password': 'test',
            'country': 'USA',
            'phone_number': '111222333444'
        })

        self.assertTrue(form.is_valid())

    # Testing employee form with no data
    def test_employee_form_no_data(self):
        form = forms.EmployeeForm(data={
        })

        self.assertFalse(form.is_valid())

    # Testing employee form with existing username
    def test_employee_form_existing_username(self):
        # The username is filled with the set up employee's object
        form = forms.EmployeeForm(data={
            'user': self.user_test,
            'first_name': 'User test',
            'last_name': 'Last name test',
            'username': 'tester',
            'email': 'email@test.com',
            'password': 'test',
            'country': 'USA',
            'phone_number': '111222333444'
        })

        # We get one error because the username already exists in the employee table.
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    # Testing employee form with less data and an employee already made with the given username
    def test_employee_form_less_data(self):
        # The username is filled with the set up employee's object
        form = forms.EmployeeForm(
            data={
                'user': self.user_test,
                'last_name': 'Last name test',
                'password': 'tester',
                'country': 'USA',
                'phone_number': '111222333444'
            })

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    # Testing today menu form with data and slack message creation
    def test_menu_form_data_today_date(self):
        form = forms.MenuForm(
            data={
                'menu_name': 'Test one',
                'created_at': date.today(),
                'menu_options': [self.option_one]
            })

        # It fails because there's already a Menu for that date
        self.assertTrue(form.is_valid())
        menu = form.save()

        # Creating slack message to send it
        form.generate_slack_message(menu.uuid)
        slack_message = SlackMessage.objects.get(created_at=date.today())
        self.assertTrue(slack_message)

        # Task which sends the message hasn't run yet
        self.assertTrue(not slack_message.sent)
        # We store if the message is sent and we verify with the message status
        sent = send_slack_message_menu()
        self.assertTrue(sent)
        slack_message = SlackMessage.objects.get(created_at=date.today())
        self.assertTrue(slack_message.sent)

        self.assertTrue(slack_message.sent == sent)

    # Testing menu with invalid date
    def test_menu_form_data_with_delta_day(self):
        modified_date = date.today() + timedelta(days=2)
        form = forms.MenuForm(
            data={
                'menu_name': 'Test one',
                'created_at': modified_date,
                'menu_options': [self.option_one]
            })

        # It fails because there's already a Menu for that date
        self.assertFalse(form.is_valid())
        # Date Created field fails
        self.assertEqual(len(form.errors), 1)

    # Testing menu for another date and slack message creation
    def test_menu_form_data_with_delta_day_plus_three(self):
        modified_date = date.today() + timedelta(days=3)
        form = forms.MenuForm(data={
            'menu_name': 'Test two',
            'created_at': modified_date,
            'menu_options': [self.option_two]
        })

        self.assertTrue(form.is_valid())
        menu = form.save()

        # Creating slack message to send it
        form.generate_slack_message(menu.uuid)
        slack_message = SlackMessage.objects.get(created_at=modified_date)
        self.assertTrue(slack_message)

        # Task which sends the message hasn't run yet
        self.assertTrue(not slack_message.sent)

    # Testing menu form with no date
    def test_menu_form_less_data(self):
        form = forms.MenuForm(data={
            'menu_name': 'Test menu',
        })

        self.assertFalse(form.is_valid())
        # Getting one error because date_created and options fields are required
        self.assertEqual(len(form.errors), 2)

    # Test order form with data
    def test_order_user_model_form_data(self):
        form = forms.MenuForm(
            data={
                'menu_name': 'Test one',
                'created_at': date.today(),
                'menu_options': [self.option_one]
            })
        menu = form.save()

        normal_time_case = datetime.now().replace(tzinfo=pytz.timezone('America/Santiago'))
        normal_time_case = normal_time_case.replace(hour=10, minute=59, second=0, microsecond=0)

        limit_time_case = datetime.now().replace(tzinfo=pytz.timezone('America/Santiago'))
        limit_time_case = limit_time_case.replace(hour=11, minute=0, second=0, microsecond=0)

        employees = Employee.objects.filter(username=self.employee.username)

        # The options belongs to today menu, if there isnt a menu, the options field is disabled
        form = forms.TestOrderForm(
            data={
                'order_customization': 'Custom observation, no salt on salad',
                'employee': self.employee,
                'created_at': normal_time_case,
                'menu_option': self.option_one
            }, menu_options=menu.menu_options, employee=employees)

        form.employee = self.employee

        self.assertTrue(form.is_valid())
        form.save()
        # Deleting the object so I can create a new one with the deadline time.
        Order.objects.get(created_at=normal_time_case).delete()

        form = forms.TestOrderForm(
            data={
                'order_customization': 'Custom observation, no salt on salad',
                'employee': self.employee,
                'created_at': limit_time_case,
                'menu_option': self.option_one
            }, menu_options=menu.menu_options, employee=employees)

        form.employee = self.employee
        self.assertFalse(form.is_valid())