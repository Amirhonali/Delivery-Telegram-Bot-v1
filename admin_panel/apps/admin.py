from django.contrib import admin

from .models import Product, Order, OrderItem, User, Category

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(User)
admin.site.register(Category)
