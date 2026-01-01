from django.shortcuts import render
from Admin.models import *

# Create your views here.

def index(request):
    # 1. Define the desired order for the TOP-LEVEL categories
    desired_order = [
        "MOBILE", 
        "LAPTOP", 
        "TABLET", 
        "PC / DESKTOP", 
        "CCTV"
    ]
    
    # 2. Fetch ONLY the Root Folders (where parent is None)
    # This ensures we don't show "Xiaomi" or "Poco" on the home page.
    root_categories = Category.objects.filter(parent__isnull=True, is_active=True)
    
    # 3. Create the mapping for sorting
    order_mapping = {name: index for index, name in enumerate(desired_order)}
    
    # 4. Sort the Root Categories
    sorted_categories = sorted(
        root_categories,
        key=lambda category: order_mapping.get(category.name.upper(), len(desired_order))
    )
    
    # 5. Pass to template. 
    # NOTE: Keep the key name 'categories' if your index.html still uses {% for category in categories %}
    context = {'categories': sorted_categories}
    return render(request, 'Falcon/index.html', context)


def about(request):
    return render(request, 'Falcon/about.html')

def contact(request):
    return render(request, 'Falcon/contact.html')
def team(request):
    return render(request, 'Falcon/team.html')
def pricing(request):
    return render(request, 'Falcon/pricing.html')
def privacy(request):
    return render(request, 'Falcon/privacy.html')
def terms(request):
    return render(request, 'Falcon/terms.html')
def maintenance(request):
    return render(request, 'Falcon/maintenance.html')
def comingsoon(request):
    return render(request, 'Falcon/coming-soon.html')
def search(request):
    return render(request, 'Falcon/search.html')
def blog(request):
    return render(request, 'Falcon/blog.html')
def error(request):
    return render(request, 'Falcon/404.html')
def faq(request):
    return render(request, 'Falcon/faq.html')
def service1(request):
    return render(request, 'Falcon/service1.html')




def elements(request):
    return render(request, 'elements.html')     



def appointment(request):
    return render(request, 'appointment.html')
def department(request):
    return render(request, 'department.html')
def departmentsingle(request):
    return render(request, 'department-single.html')
def doctor(request):
    return render(request, 'doctor.html')
def doctorsingle(request):
    return render(request, 'doctor-single.html')

def gallery(request):
    return render(request, 'gallery.html')
def testimonial(request):
    return render(request, 'testimonial.html')


