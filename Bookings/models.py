from django.db import models

# Create your models here.
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Technician Assigned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    user = models.ForeignKey('Accounts.MyUser', on_delete=models.CASCADE)
    service_type = models.CharField(max_length=100)
    service_name = models.CharField(max_length=200)
    model = models.CharField(max_length=100)
    purpose = models.CharField(max_length=100)
    description = models.TextField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    booking_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Tracking
    sequence_number = models.PositiveIntegerField(unique=True, editable=False)
    token = models.CharField(max_length=30, editable=False, null=True, blank=True)
    order_id = models.CharField(max_length=10, editable=False, null=True, blank=True)
    

    def save(self, *args, **kwargs):
        if not self.pk:
            # 1. Generate sequence number
            last = Booking.objects.order_by('-sequence_number').first()
            self.sequence_number = last.sequence_number + 1 if last else 1
            counter = f"{self.sequence_number:04d}"

            # 2. Build token parts
            # Logic: ST(2) + SN(3) + MD(Last 3) + Counter
            st = (self.service_type or "XX")[:2].title()
            sn = (self.service_name or "XXX")[:3].title()
            # Remove spaces from model and take last 3 chars
            clean_model = (self.model or "MOD").replace(" ", "")
            md = clean_model[-3:].upper() if len(clean_model) >= 3 else clean_model.upper()

            self.token = f"{st}{sn}{md}{counter}"
            self.order_id = f"#{counter}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_id} - {self.service_name} ({self.user.username})"


class BookingAddress(models.Model):
    # Use related_name='address' for easier access in templates
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='address')
    
    # New Fields from your Form
    house_no = models.CharField(max_length=100)
    building_name = models.CharField(max_length=100)
    
    street = models.CharField(max_length=255)
    landmark = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, default="Bangalore")
    state = models.CharField(max_length=100, default="Karnataka")
    pincode = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='India')

    def __str__(self):
        return f"Address for {self.booking.order_id}"

class BookingStatus(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)  # e.g., Pending, Confirmed, Completed, Cancelled
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Status of Booking ID {self.booking.id}: {self.status}"
    



