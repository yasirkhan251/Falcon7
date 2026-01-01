
from django.contrib import admin
from .models import ServiceCategory, ServiceProduct

# ============================================================
# SERVICE CATEGORY ADMIN
# ============================================================

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at", "updated_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}  # Auto fill slug in admin UI
    readonly_fields = ("created_at", "updated_at")
    ordering = ("name",)

# ============================================================
# SERVICE PRODUCT ADMIN
# ============================================================

@admin.register(ServiceProduct)
class ServiceProductAdmin(admin.ModelAdmin):
    list_display = ("Product", "SC", "slug", "price", "is_active", "created_at")
    list_filter = ("SC", "is_active")
    search_fields = ("Product__model_name", "SC__name", "slug")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("Product__model_name",)
