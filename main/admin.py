from django.contrib import admin
from .models import *

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class FoodAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('foodname',)}
    list_display = ['id', 'type', 'foodname', 'price', 'pix', 'special_gifts', 'uploaded_at', 'updated_at']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'email', 'phone',]

class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'food', 'qty', 'amount', 'paid',]

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'phone', 'paid', 'purchase_date',]


admin.site.register(AppInfo)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Contact)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Purchase, PurchaseAdmin)

