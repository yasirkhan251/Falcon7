from django.urls import path
from . import views

urlpatterns = [
    path('Admin_dashboard/', views.Admin_dashboard, name='Admin_dashboard'),
    path('Admin_products/', views.Admin_products, name='Admin_products'),
    
    path('Admin_products/<int:category_id>/', views.Admin_products, name='Admin_products_folder'),
    
    # This is the specific line you are missing or has a typo:
    path('category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('category/delete/<int:pk>/', views.delete_category, name='delete_category'),
    
    path('product/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:pk>/', views.delete_product, name='delete_product'),
    
    path('add-folder/', views.add_folder, name='add_folder'),
    path('add-product/', views.add_product, name='add_product'),
    path('update-order/', views.update_display_order, name='update_display_order'),
    path('bookinglist/', views.bookinglist, name='bookinglist'),
    path('booking/edit/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('booking/delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
]