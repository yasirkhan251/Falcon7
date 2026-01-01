from django.shortcuts import render
from Admin.models import Category
from .models import *
from django.shortcuts import render, get_object_or_404
# Create your views here.
def folder_view(request, slug=None):
    """
    Handles everything: Root level, Sub-folders, and Product listings.
    """
    if slug is None:
        # ROOT LEVEL: Show Mobile, Laptop, etc.
        current_folder = None
        children = Category.objects.filter(parent__isnull=True, is_active=True)
        products = []
    else:
        # INSIDE A FOLDER: Show sub-folders (like Xiaomi) or Products (like Mi 11)
        current_folder = get_object_or_404(Category, slug=slug)
        children = current_folder.children.filter(is_active=True)
        products = current_folder.products.filter(is_active=True)

    context = {
        'current_folder': current_folder,
        'sub_folders': children,
        'products': products,
    }
    return render(request, 'service/list_view.html', context)
    
    
def service_detail(request, product_id):
    """
    Shows the services (Screen repair, Battery, etc.) for one specific product.
    """
    product = get_object_or_404(Product, id=product_id)
    
    # Get all service options linked to this specific product
    services = ServiceProduct.objects.filter(Product=product)
    service_categories = ServiceCategory.objects.all()

    context = {
        'product': product,
        'services': services,
        'service_categories': service_categories,
        'category': product.category, # This allows breadcrumbs
    }
    return render(request, 'service/service_for.html', context)
    