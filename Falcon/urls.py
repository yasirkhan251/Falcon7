from django.urls import path,include,reverse
from .views import *    
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
       path('', index, name='index'),
       path('service1/', service1, name='service1'),
       path('about/', about, name='about'),
     
       path('contact/', contact, name='contact'),
       path('team/', team, name='team'),
       path('pricing/', pricing, name='pricing'),
       path('privacy/', privacy, name='privacy'),
       path('terms/', terms, name='terms'),
       path('maintenance/', maintenance, name='maintenance'),
       path('comingsoon/', comingsoon, name='comingsoon'),
       path('search/', search, name='search'),
       path('blog/', blog, name='blog'),
       path('error/', error, name='error'),
       path('faq/', faq, name='faq'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)