from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # The Root (Mobile, Laptop, etc.)
    path('', folder_view, name='service_root'),
    
    # Any subfolder (Xiaomi, Poco, etc.)
    path('<slug:slug>/', folder_view, name='folder_detail'),
    
    # The final service page for a product
    path('service-details/<int:product_id>/', service_detail, name='service_detail'),
    path('update-order/', update_display_order, name='update_display_order'),
]



#    path('category/<slug:slug>/', category_detail, name='category_detail'),
# This name must match the 'category_detail' used in the template

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)