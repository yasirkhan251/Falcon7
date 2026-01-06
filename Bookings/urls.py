from django.urls import path
from .views import *



urlpatterns = [
path("booking/<type>/<company>/<model>/<purposes>/", bookings_view, name="bookings"),
path("booking/success/<int:booking_id>/", booking_success, name="booking_success"),
path("booking/menu/<product>/<service>/", booking_menu, name="booking_menu"),

#    path('category/<slug:slug>/', category_detail, name='category_detail'),
# This name must match the 'category_detail' used in the template
]