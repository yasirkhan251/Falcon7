from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'service_type',
        'service_name',
        'model',
        'purpose',
        'booking_date',
        'created_at',
    )

    list_filter = (
        'service_type',
        'booking_date',
        'created_at',
    )

    search_fields = (
        'user__username',
        'service_name',
        'service_type',
        'model',
        'purpose',
    )

    ordering = ('-created_at',)

    readonly_fields = ('created_at',)

