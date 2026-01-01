from django.db import models

# Create your models here.
class Booking(models.Model):
    user = models.ForeignKey('Accounts.MyUser', on_delete=models.CASCADE)
    service_type = models.CharField(max_length=100)
    service_name = models.CharField(max_length=200)
    model = models.CharField(max_length=100)
    purpose =  models.CharField(max_length=100)
    description = models.TextField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    booking_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    sequence_number = models.PositiveIntegerField(unique=True, editable=False)
    token = models.CharField(max_length=30, editable=False, null=True   , blank=True)
    order_id = models.CharField(max_length=6, editable=False, null=True   , blank=True)
    def save(self, *args, **kwargs):
        if not self.pk:
            # ---- generate next sequence number ----
            last = Booking.objects.order_by('-sequence_number').first()
            self.sequence_number = last.sequence_number + 1 if last else 1

            # ---- format counter ----
            counter = f"{self.sequence_number:04d}"

            # ---- build token parts ----
            st = (self.service_type or "")[:2].title()           # Mo
            sn = (self.service_name or "")[:3].title()           # Sam
            md = (self.model or "").replace(" ", "")[-3:].upper()  # S24

            # ---- final values ----
            self.token = f"{st}{sn}{md}{counter}"
            self.order_id = f"#{counter}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking for {self.service_name} by {self.user.username} on {self.booking_date}"
    
class BookingAddress(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    landmark = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=100 )
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='India')
    

    def __str__(self):
        return f"Address for Booking ID {self.booking.id}: {self.street}, {self.city}"

class BookingStatus(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)  # e.g., Pending, Confirmed, Completed, Cancelled
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Status of Booking ID {self.booking.id}: {self.status}"
    