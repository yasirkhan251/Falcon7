from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.db import transaction
from Admin.models import Category, Product
from services.models import ServiceCategory, ServiceProduct 
from .models import Booking, BookingAddress
from datetime import datetime
# Create your views here.



@login_required
def bookings_view(request, product, service):
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



def booking_menu(request, product, service):
    # 1. Fetch the Product and Category Path (Your existing logic)
    product_obj = get_object_or_404(
        Product.objects.select_related('category__parent__parent'), 
        sku=product
    )
    category_path = product_obj.category.get_path_list()

    if request.method == 'POST':
        # 2. Extract Timing Data (New logic)
        date_val = request.POST.get('booking_date')
        hour_val = request.POST.get('booking_hour') # Coming as 10, 14, 20 etc. from JS
        
        try:
            # Combine into Python datetime
            combined_dt = datetime.strptime(f"{date_val} {hour_val}:00", '%Y-%m-%d %H:%M')
            
            # 3. Use Atomic Transaction to save both models together
            with transaction.atomic():
                # Create the Main Booking
                # We pull service_type from the root of your category_path
                booking = Booking.objects.create(
                    user=request.user,
                    service_type=category_path[0].name, # e.g., "Mobile"
                    service_name=product_obj.brand,     # e.g., "Samsung"
                    model=product_obj.model_name,       # e.g., "S24 Ultra"
                    purpose=service,                    # e.g., "repair"
                    description=request.POST.get('description'),
                    phone=request.POST.get('phone'),
                    booking_date=combined_dt
                )

                # Create the Booking Address
                BookingAddress.objects.create(
                    booking=booking,
                    street=request.POST.get('street'),
                    landmark=request.POST.get('landmark'),
                    city=request.POST.get('city'),
                    pincode=request.POST.get('pincode'),
                    # We can store house/building in the street field 
                    # or update your model to include them separately
                    state="Karnataka" 
                )

            messages.success(request, f"Booking confirmed! Order ID: {booking.order_id}")
            return redirect('booking_success', token=booking.token) # Replace with your actual URL name

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    # Context for the GET request (Your existing logic)
    context = {
        'sku_str': product,
        'service': service,
        'product': product_obj,
        'category_path': category_path 
    }

    return render(request, 'Bookings/bookings.html', context)


def booking_success(request, token):
    # Fetch the booking using the unique token
    # Use select_related to get the address in the same query
    booking = get_object_or_404(Booking.objects.select_related('address'), token=token)
    
    return render(request, 'Bookings/success.html', {'booking': booking})



@login_required
def my_bookings(request):
    # Fetch bookings for the logged-in user
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'bookings': bookings,
    }
    return render(request, 'Bookings/my_bookings.html', context)