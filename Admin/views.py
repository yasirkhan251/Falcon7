# from django.shortcuts import render, redirect, get_object_or_404
# from django.utils.text import slugify
# from .models import Category, Product

# def admin_dashboard(request, category_id=None):
#     if category_id:
#         current_folder = get_object_or_404(Category, id=category_id)
#         sub_folders = current_folder.children.all()
#         files = current_folder.products.all()
#     else:
#         current_folder = None
#         sub_folders = Category.objects.filter(parent__isnull=True)
#         files = [] # Root usually only has folders

#     return render(request, 'admin/dashboard.html', {
#         'current_folder': current_folder,
#         'sub_folders': sub_folders,
#         'files': files
#     })

# def add_folder(request):
#     if request.method == "POST":
#         name = request.POST.get('name')
#         parent_id = request.POST.get('parent_id')
#         parent = Category.objects.get(id=parent_id) if parent_id else None
        
#         Category.objects.create(
#             name=name,
#             parent=parent,
#             slug=slugify(name)
#         )
#         return redirect('admin_dashboard_folder', category_id=parent_id) if parent_id else redirect('admin_dashboard')

# def add_product(request):
#     if request.method == "POST":
#         cat_id = request.POST.get('category_id')
#         category = get_object_or_404(Category, id=cat_id)
        
#         Product.objects.create(
#             category=category,
#             brand=request.POST.get('brand'),
#             model_name=request.POST.get('model_name'),
#             price=request.POST.get('price'),
#             stock=request.POST.get('stock'),
#             # Image handling would go here
#         )
#         return redirect('admin_dashboard_folder', category_id=cat_id)



from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product

def admin_dashboard(request, category_id=None):
    if category_id:
        current_folder = get_object_or_404(Category, id=category_id)
        sub_folders = current_folder.children.all()
        files = current_folder.products.all()
    else:
        current_folder = None
        sub_folders = Category.objects.filter(parent__isnull=True)
        files = []

    return render(request, 'Admin/dashboard.html', {
        'current_folder': current_folder,
        'sub_folders': sub_folders,
        'files': files
    })

def add_folder(request):
    if request.method == "POST":
        name = request.POST.get('name')
        parent_id = request.POST.get('parent_id')
        parent = Category.objects.get(id=parent_id) if parent_id else None
        
        Category.objects.create(name=name, parent=parent)
        
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
            stock=request.POST.get('stock')
        )
        return redirect('admin_dashboard_folder', category_id=cat_id)
    return redirect('admin_dashboard')