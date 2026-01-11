"""
URL configuration for hello project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path 
from inventory import views 

admin.site.site_header = "Inventory Management Admin"
admin.site.site_title = "Inventory Management Admin Portal"
admin.site.index_title = "Welcome to Inventory Management Portal"


urlpatterns = [
    path("",views.dashboard, name="Dashboard"),
    path("Inventory",views.Inventory, name="Inventory"),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    path("Sales",views.Sales, name="Sales"),
    path("DemandForecasting",views.DemandForecasting, name="DemandForecasting"),
    path("PurchasePlan",views.PurchasePlan, name="PurchasePlan"),
    path("SmartAlerts",views.SmartAlerts, name="SmartAlerts"),
    path("DownloadReports",views.DownloadReports, name="DownloadReports"),
    path('download/inventory/csv/', views.download_inventory_csv, name='download_inventory_csv'),
    path('download/sales/csv/', views.download_sales_csv, name='download_sales_csv'),
]
