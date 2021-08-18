from django.urls import path
from . import views


app_name = 'yumminess'
urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('dashboard', views.Dashboard.as_view(), name='dashboard'),
    path('employee/list', views.EmployeeListView.as_view(), name='employee-list'),
    path('employee/create', views.EmployeeCreateView.as_view(), name='employee-create'),
    path('employee/<int:pk>', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('employee/<int:pk>/update', views.EmployeeUpdateView.as_view(), name='employee-update'),

]