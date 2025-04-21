from django.contrib import admin
from shop.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Category model.

    Automatically generates the slug from the category name.
    Displays name and slug in the admin list view.
    """
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Product model.

    Allows inline editing of price and status,
    filtering by status and creation date,
    and includes a custom bulk action for changing status.
    """
    list_display = ('name', 'price', 'status')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('status', 'created')
    list_editable = ('price', 'status')
    raw_id_fields = ('category',)
    actions = ('change_status',)

    @admin.action(description='Mark selected products as active')
    def change_status(self, request, queryset):
        """
        Custom admin action to set the 'status' field to True for selected products.
        """
        rows_count = queryset.update(status=True)
        self.message_user(request, f'{rows_count} product(s) were marked as active.')
