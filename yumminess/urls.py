from django.urls import path
from . import views
from .decorators import unauthenticated_user


app_name = 'yumminess'
urlpatterns = [
    path('login', unauthenticated_user(views.LoginView.as_view()), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('dashboard', views.Dashboard.as_view(), name='dashboard'),
    path('employee/list', views.EmployeeListView.as_view(), name='employee_list'),
    path('employee/create', views.EmployeeCreateView.as_view(), name='employee_create'),
    path('employee/<int:pk>', views.EmployeeDetailView.as_view(), name='employee_detail'),
    path('employee/<int:pk>/update', views.EmployeeUpdateView.as_view(), name='employee_update'),
    path('employee/<int:pk>/delete', views.EmployeeDeleteView.as_view(), name='employee_delete'),
    path('menu_option_plate/list', views.MenuOptionPlateListView.as_view(), name='menu_option_plate_list'),
    path('menu_option_plate/create', views.MenuOptionPlateCreateView.as_view(), name='menu_option_plate_create'),
    path('menu_option_plate/<int:pk>', views.MenuOptionPlateDetailView.as_view(), name='menu_option_plate_detail'),
    path('menu_option_plate/<int:pk>/update', views.MenuOptionPlateUpdateView.as_view(), name='menu_option_plate_update'),
    path('menu_option_plate/<int:pk>/delete', views.MenuOptionPlateDeleteView.as_view(), name='menu_option_plate_delete'),
    path('menu_option/list', views.MenuOptionListView.as_view(), name='menu_option_list'),
    path('menu_option/create', views.MenuOptionCreateView.as_view(), name='menu_option_create'),
    path('menu_option/<int:pk>', views.MenuOptionDetailView.as_view(), name='menu_option_detail'),
    path('menu_option/<int:pk>/update', views.MenuOptionUpdateView.as_view(), name='menu_option_update'),
    path('menu_option/<int:pk>/delete', views.MenuOptionDeleteView.as_view(), name='menu_option_delete'),
    path('menu/list', views.MenuListView.as_view(), name='menu_list'),
    path('menu/create', views.MenuCreateView.as_view(), name='menu_create'),
    path('menu/<int:pk>', views.MenuDetailView.as_view(), name='menu_detail'),
    path('menu/<slug:menu_uuid>', views.MenuDetailView.as_view(), name='menu_detail'),
    path('menu/<int:pk>/update', views.MenuUpdateView.as_view(), name='menu_update'),
    path('menu/<int:pk>/delete', views.MenuDeleteView.as_view(), name='menu_delete'),
    path('order/list', views.OrderListView.as_view(), name='order_list'),
    path('order/create', views.OrderCreateView.as_view(), name='order_create'),
    path('order/<int:pk>', views.OrderDetailView.as_view(), name='order_detail'),
    path('order/<int:pk>/update', views.OrderUpdateView.as_view(), name='order_update'),
    path('order/<int:pk>/delete', views.OrderDeleteView.as_view(), name='order_delete'),

]