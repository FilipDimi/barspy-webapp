from django.contrib import admin
from django.urls import path
from core import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('783edho8d234das', views.adminPanel, name="adminPanel"),
    path('32d3d234f23cs1e', views.send_alert, name="send_alert"),
    path('add_category', views.add_category, name="add_category"),
    path('add_sub', views.add_sub, name="add_sub"),
    path('add_drink', views.add_drink, name="add_drink"),

    path('', views.index, name='index'),
    path('history', views.history, name='history'),
    path('inventory', views.inventory, name='inventory'),
    path('checkin', views.checkin, name='checkin'),
    path('checkinDetails/<int:pk>', views.checkinDetails, name='checkinDetails'),
    path('history/<int:pk>', views.transactions_per_day, name='transactions_per_day'),
    path('add_transaction', views.add_transaction, name='add_transaction'),
    path('add_checkin', views.add_checkin, name='add_checkin'),
    path('send_report', views.send_report, name='send_report'),
    path('toggleEmergency/<int:pk>', views.toggleEmergency, name="toggleEmergency"),
    # Auth
    path('login', views.login, name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
]
