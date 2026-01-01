from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # This shows the path like: Mobile > Xiaomi > Poco in the list
    list_display = ('name', 'get_path', 'parent', 'display_order', 'is_active')
    list_filter = ('parent', 'is_active')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('parent', 'display_order', 'name')

    def get_path(self, obj):
        # This uses the method we added in the model
        return obj.get_full_path()
    get_path.short_description = 'Full Directory Path'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'brand', 'get_category_path', 'price', 'stock', 'is_active')
    list_filter = ('brand', 'category', 'is_active')
    search_fields = ('model_name', 'brand', 'sku')
    
    # This helps you see exactly which folder the product is in
    def get_category_path(self, obj):
        return obj.category.get_full_path()
    get_category_path.short_description = 'Folder Location'