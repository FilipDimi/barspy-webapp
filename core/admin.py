from django.contrib import admin
from .models import Category, SubCategory, Drink, Transaction, History, CheckIn

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Drink)
admin.site.register(Transaction)
admin.site.register(History)
admin.site.register(CheckIn)