from django.contrib import admin
from . models import Order,Address,DetilOrder,Like
# Register your models here.
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(DetilOrder)
admin.site.register(Like)
