from django.shortcuts import render
from Admin.models import Category
from .models import *
from django.shortcuts import render, get_object_or_404
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
    
    
def service_detail(request, product_id ):
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
        'pids': product_id,
        'category': product.category, # This allows breadcrumbs
    }
    return render(request, 'service/service_for.html', context)
     


def update_display_order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        items = data.get('items', [])

        for item in items:
            item_id = item.get('id')
            new_order = item.get('order')
            
            if item.get('type') == 'folder':
                Category.objects.filter(id=item_id).update(display_order=new_order)
            else:
                # If your product model also has display_order
                Product.objects.filter(id=item_id).update(display_order=new_order)

        return JsonResponse({'status': 'success'})
    

    