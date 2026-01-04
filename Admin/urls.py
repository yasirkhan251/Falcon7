from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/<int:category_id>/', views.admin_dashboard, name='admin_dashboard_folder'),
    
    # This is the specific line you are missing or has a typo:
    path('category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('category/delete/<int:pk>/', views.delete_category, name='delete_category'),
    
    path('product/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:pk>/', views.delete_product, name='delete_product'),
    
    path('add-folder/', views.add_folder, name='add_folder'),
    path('add-product/', views.add_product, name='add_product'),
    path('update-order/', views.update_display_order, name='update_display_order'),
]