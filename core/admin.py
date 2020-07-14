from django.contrib import admin

from .models import Recipe, OrderRecipe, Order

admin.site.register(Recipe)
admin.site.register(OrderRecipe)
admin.site.register(Order)
# Register your models here.
