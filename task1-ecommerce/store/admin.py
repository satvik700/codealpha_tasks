from django.contrib import admin
from .models import Product, Order, OrderItem
class ItemInline(admin.TabularInline):
    model = OrderItem; extra = 0
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [ItemInline]; list_display = ("id","user","total","created")
admin.site.register(Product)
