from django.urls import path
from . import views
from .decorators import unauthenticated_user


app_name = 'yumminess'
urlpatterns = [
    path('login', unauthenticated_user(views.LoginView.as_view()), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('dashboard', views.Dashboard.as_view(), name='dashboard'),
    path('employee/list', views.EmployeeListView.as_view(), name='employee-list'),
    path('employee/create', views.EmployeeCreateView.as_view(), name='employee-create'),
    path('employee/<int:pk>', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('employee/<int:pk>/update', views.EmployeeUpdateView.as_view(), name='employee-update'),
    path('employee/<int:pk>/delete', views.EmployeeDeleteView.as_view(), name='employee-delete'),
    path('menu-plate/list', views.MenuPlateListView.as_view(), name='menu-plate-list'),
    path('menu-plate/create', views.MenuPlateCreateView.as_view(), name='menu-plate-create'),
    path('menu-plate/<int:pk>', views.MenuPlateDetailView.as_view(), name='menu-plate-detail'),
    path('menu-plate/<int:pk>/update', views.MenuPlateUpdateView.as_view(), name='menu-plate-update'),
    path('menu-plate/<int:pk>/delete', views.MenuPlateDeleteView.as_view(), name='menu-plate-delete'),
    path('menu-option/list', views.MenuOptionListView.as_view(), name='menu-option-list'),
    path('menu-option/create', views.MenuOptionCreateView.as_view(), name='menu-option-create'),
    path('menu-option/<int:pk>', views.MenuOptionDetailView.as_view(), name='menu-option-detail'),
    path('menu-option/<int:pk>/send-slack', views.MenuOptionDetailView.as_view(), name='menu-option-detail'),
    path('menu-option/<int:pk>/update', views.MenuOptionUpdateView.as_view(), name='menu-option-update'),
    path('menu-option/<int:pk>/delete', views.MenuOptionDeleteView.as_view(), name='menu-option-delete'),
    path('menu/list', views.MenuListView.as_view(), name='menu-list'),
    path('menu/create', views.MenuCreateView.as_view(), name='menu-create'),
    path('menu/<int:pk>', views.MenuDetailView.as_view(), name='menu-detail'),
    path('menu/<slug:menu_uuid>', views.MenuDetailView.as_view(), name='menu-detail'),
    path('menu/<int:pk>/update', views.MenuUpdateView.as_view(), name='menu-update'),
    path('menu/<int:pk>/delete', views.MenuDeleteView.as_view(), name='menu-delete'),
    path('order/list', views.OrderListView.as_view(), name='order-list'),
    path('order/create', views.OrderCreateView.as_view(), name='order-create'),
    path('order/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('order/<int:pk>/update', views.OrderUpdateView.as_view(), name='order-update'),
    path('order/<int:pk>/delete', views.OrderDeleteView.as_view(), name='order-delete'),

]