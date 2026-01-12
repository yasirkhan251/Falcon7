from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Category, Product
from Bookings.models import Booking, BookingAddress
from Accounts.models import MyUser
import json


def Admin_dashboard(request):
    bookings = Booking.objects.all().order_by('-created_at') # Newest first
    bookings_count = bookings.count()
    
    bookings_pending = bookings.filter(status='pending')
    bookings_pending_count = bookings_pending.count()
    
    # Efficiently getting addresses related to these bookings
    bookings_addresses = BookingAddress.objects.filter(booking__in=bookings)
    
    clients = MyUser.objects.filter(is_admin=False)
    clientscount = clients.count()

    bookings_today = bookings.filter(created_at__date=date.today())
    bookings_today_count = bookings_today.count()

    context = {
        'bookings_count': bookings_count,
        'clientscount': clientscount,
        'bookings_pending_count': bookings_pending_count,
        'bookings_addresses': bookings_addresses,   
        'recent_bookings': bookings[:5],  # Sending the 10 latest to the table
        'clients': clients,
        'bookings_today_count': bookings_today_count,
    }
    
    return render(request, 'Admin/Admin_dashboard.html', context)
    
# Edit View
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        # Example: Updating status
        booking.status = request.POST.get('status')
        booking.save()
        return redirect('Admin_dashboard')
    
    return render(request, 'Admin/edit_booking.html', {'booking': booking})

# Delete View
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.delete()
    return redirect('Admin_dashboard')

def Admin_products(request, category_id=None):
    if category_id:
        current_folder = get_object_or_404(Category, id=category_id)
        # Fix: Ensure these match the related_names in your models.py
        sub_folders = current_folder.children.all().order_by('display_order')
        files = current_folder.products.all().order_by('display_order')
    else:
        current_folder = None
        sub_folders = Category.objects.filter(parent__isnull=True).order_by('display_order')
        files = []

    return render(request, 'Admin/Admin_products.html', {
        'current_folder': current_folder,
        'sub_folders': sub_folders,
        'files': files
    })

def add_folder(request):
    if request.method == "POST":
        name = request.POST.get('name')
        parent_id = request.POST.get('parent_id')
        image = request.FILES.get('image')
        description = request.POST.get('description')
        
        parent = Category.objects.get(id=parent_id) if parent_id else None
        Category.objects.create(name=name, parent=parent, image=image, description=description)
        
        # FIX: Changed 'category_id' to match your admin_dashboard parameter
        if parent_id:
            return redirect('admin_dashboard_folder', category_id=parent_id)
    return redirect('admin_dashboard')

def add_product(request):
    if request.method == "POST":
        cat_id = request.POST.get('category_id')
        category = get_object_or_404(Category, id=cat_id)
        
        Product.objects.create(
            category=category,
            brand=request.POST.get('brand'),
            model_name=request.POST.get('model_name'),
            price=request.POST.get('price'),
            stock=request.POST.get('stock'),
            image=request.FILES.get('image') # Added image support
        )
        return redirect('admin_dashboard_folder', category_id=cat_id)
    return redirect('admin_dashboard')

def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.name = request.POST.get('name')
        category.description = request.POST.get('description')
        if request.FILES.get('image'):
            category.image = request.FILES.get('image')
        category.save()
        
        # FIX: Unified parameter name to category_id
        if category.parent:
            return redirect('admin_dashboard_folder', category_id=category.parent.id)
        return redirect('admin_dashboard')

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.brand = request.POST.get('brand')
        product.model_name = request.POST.get('model_name')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
        product.save()
        # FIX: Unified parameter name to category_id
        return redirect('admin_dashboard_folder', category_id=product.category.id)

def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    parent_id = category.parent.id if category.parent else None
    category.delete()
    
    if parent_id:
        return redirect('admin_dashboard_folder', category_id=parent_id)
    return redirect('admin_dashboard')

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    category_id = product.category.id
    product.delete()
    return redirect('admin_dashboard_folder', category_id=category_id)

# Added the missing drag-and-drop view
def update_display_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        for item in data.get('items', []):
            if item['type'] == 'folder':
                Category.objects.filter(id=item['id']).update(display_order=item['order'])
            else:
                Product.objects.filter(id=item['id']).update(display_order=item['order'])
        return JsonResponse({'status': 'success'})
    


def bookinglist(request):
    bookings = Booking.objects.all()
    booking_addresses = BookingAddress.objects.filter(booking__in=bookings)     
    context = {
        'bookings': bookings,
        'booking_addresses': booking_addresses
    }

    return render(request, 'Admin/bookinglist.html', context)