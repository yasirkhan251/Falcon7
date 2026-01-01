from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    # The self-referencing link (Folder concept)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children'
    )
    
    # Metadata
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        # Prevents two sub-folders having the same name in the same parent folder
        unique_together = ('parent', 'name')
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

    def get_full_path(self):
        """Returns the breadcrumb path as a string"""
        full_path = [self.name]
        p = self.parent
        while p is not None:
            full_path.append(p.name)
            p = p.parent
        return ' / '.join(full_path[::-1])

    def save(self, *args, **kwargs):
        if not self.slug:
            # We add parent name to slug to ensure uniqueness (e.g., /phones/cases vs /laptops/cases)
            prefix = f"{self.parent.name}-" if self.parent else ""
            self.slug = slugify(f"{prefix}{self.name}")
        super().save(*args, **kwargs)


class Product(models.Model):
    # This points to the specific "Folder" the file is in
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products'
    )
    
    brand = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    variant = models.CharField(max_length=50, blank=True, null=True)
    
    # Visuals and Info
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    # Inventory and Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True, editable=False)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.sku:
            # Dynamic SKU generation based on brand and model
            brand_part = self.brand[:3].upper()
            model_part = slugify(self.model_name)[:10].upper()
            self.sku = f"FTW-{brand_part}-{model_part}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} {self.model_name}"