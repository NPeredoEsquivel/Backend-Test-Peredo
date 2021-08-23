# Backend-Test-Peredo

Welcome to Yumminess project. The main goal of Yumminess is to coordinate the chilean employees menu, sending a slack message everyday at 10:00 am CLT with the menu of it day. The employee can access to the link of the message and choose the menu. The link is public, anybody can see it, but only the users can place the order for the menu (Yup, Yumminess manages user auth).
The main actor of the app is Nora, she manages all the plates, options, menu, orders and employees.

The project was programmed with python, using Django 3.0.8, Celery 4.3.0, Redis 3.5.3 and the test were handled with unit and integration testing. Celery was used to schedule the periodically tasks and redis as a message broker, who handles the tasks with workers. 

## Project configuration.
To configure the project, please follow the next steps.

- Create the directory to clone and clone the project.
- Access to the project directory  
- Create virtual environment.
- Activate virtual environment.
- Install the requirements (pip install -r requeriments.txt)
- Generate the migration files (python manage.py makemigrations).
- Apply migrations (python manage.py migrate).
- Create Nora (python manage.py createsuperuser).

## Base project configuration
To configure base project variable, you need to change BASE_URL in settings.py (default is "http://localhost:8000/").

```
BASE_URL = "http://localhost:8000/"
```

##Webhook configuration
To send messages to slack workspace, the project uses webhooks and to activate the periodic task, you need to have a slack application (If you dont have one go to this url and follow the step by step https://api.slack.com/apps). Having the workspace configured, you need to obtain the 
Webhook URL (i.e https://hooks.slack.com/services/XXXXXXX/XXXXXXX/XXXXXXXXXXXXXX). If you already have one, you need to place the hook url in settings.py.

```
SLACK_WEB_HOOK = https://hooks.slack.com/services/XXXXXXXXXX/XXXXXXXXXXX/XXXXXXXXXXXXXXXXXXXXXXXX.
```

##Project flow
The project is very intuitive, but here are some explanations of what can Nora do. Logging in with nora, you can feed this project with data. The flow is to make the menu option plates first to assign them to the menu options, after this you can create a different kind of menu with the different options. You can create employees too, they're the another importants actors in the system, because the main goal is to manage the menus for them so they can have the meal on time and well served. When you create employees with Nora, you create employees with some backend logic, so employees can login to the application. Now the employees can order a menu with a datetime threshold of 11:00 am CLT.

Nora can create only one menu per day, and the orders has the options of that menu only. And when the menu is being made, a slack message is created in the backend so when the time comes to send the message with the periodic task it will handle it correctly. This message have an status, false when the message haven't being sent and true otherwise.

The menu has a detail view which can be acceded by the employees, they can be logged in or not, doesn't mind. Because the menu has an special attribute which is an UUID. The url with the UUID is sent in the message.

##Celery periodic task
To activate the periodic task, you need to configure some params.
The settings.py obtains some env variables, and in this case docker wasn't used, so you need to export the variables to your env has follows:

In your terminal execute this:
```
export CELERY_BROKER_URL='redis://localhost:6379'
export CELERY_RESULT_BACKEND_URL='redis://localhost:6379'
```
This tells celery to send the messages to redis in local.

And to activate the beat scheduler so celery can send the task to redis, you need to open three new terminals, one for celery worker, another for celery beat scheduler and the third one for redis server.

```
 celery -A backend_test worker -l info
 celery -A backend_test beat -l info
 redis-server
```
(You can test redis with redis-cli  PING, it should return PONG).

And finally but not least, the tests. There's a lot of unit test, handling users auth and forms. And the most important, the messages with the options. It verifys if a message have being sent with a flag and verifies the behaviour of it.

Any doubt, don't hesitate to contact me at +569 96679440 or my personal email nperedoesquivel@gmail.com.
