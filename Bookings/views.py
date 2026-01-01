from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Booking, BookingAddress
# Create your views here.



@login_required
def bookings_view(request, type, company, model, purposes):
    if request.method == 'POST':
        # 1. Capture Booking Data into temporary variables
        service_type = request.POST.get('service_type_val') # Note: your inputs were 'disabled', 
        service_name = request.POST.get('service_name_val') # so use hidden inputs or pass them via context
        model_device = request.POST.get('model_val')
        purpose = request.POST.get('purpose_val')
        phone = request.POST.get('phone')
        booking_date = request.POST.get('booking_date')
        description = request.POST.get('description')
        token = request.POST.get('csrfmiddlewaretoken')
        

        # 2. Capture Address Data into temporary variables
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        landmark = request.POST.get('landmark')




        # Basic Validation
        if not all([booking_date, street, city, pincode]):
            messages.error(request, "Please fill in all required fields marked with *")
            return redirect(request.path)

        try:
            # 3. Use an atomic transaction to save to both tables
            with transaction.atomic():
                # Save Primary Booking Table
                new_booking = Booking.objects.create(
                    user=request.user,
                    service_type=service_type,
                    service_name=service_name,
                    model=model_device,
                    purpose=purpose,
                    description=description,
                    phone=phone,
                    booking_date=booking_date
                )

                # Save Linked Address Table
                BookingAddress.objects.create(
                    booking=new_booking,
                    street=street,
                    landmark=landmark,
                    city=city,
                    state=state,
                    pincode=pincode
                )

            messages.success(request, "Service booked successfully! Our team will contact you soon.")
            return redirect("booking_success", booking_id=new_booking.id)

        except Exception as e:
            print(f"Booking Error: {e}")
            messages.error(request, "An error occurred while saving your booking. Please try again.")
    context = {
        'type': type,
        'company': company,
        'model': model,
        'purposes': purposes
    }
    # If GET request, render the form (you may need to pass initial data here)
    return render(request, 'Bookings/bookings.html', context)




@login_required
def booking_success(request, booking_id):
    booking = Booking.objects.select_related().get(id=booking_id)
    address = BookingAddress.objects.get(booking=booking)

    context = {
        "booking": booking,
        "address": address,
    }
    return render(request, "Bookings/booking_success.html", context)