from django.urls import path,include,reverse
from .views import *    
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/<int:category_id>/', admin_dashboard, name='admin_dashboard_folder'),
    path('add-folder/', add_folder, name='add_folder'),
    path('add-product/', add_product, name='add_product'),
]