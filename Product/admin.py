from django.contrib import admin
from .models import Product,DetailProduct,System,Phone , Comment,Pooshak,DetailPooshak,Oven,Bag,Cover,Laundry,TV,Refrigerator,Categorize_Products,ImageCategorize,ImageProduct,BrandProduct

admin.site.register(Product)
admin.site.register(DetailProduct)
admin.site.register(System)
admin.site.register(Phone)
admin.site.register(Comment)
admin.site.register(Pooshak)
admin.site.register(DetailPooshak)
admin.site.register(TV)
admin.site.register(Refrigerator)
admin.site.register(Laundry)
admin.site.register(Oven)
admin.site.register(Bag)
admin.site.register(Cover)
admin.site.register(Categorize_Products)
admin.site.register(ImageCategorize)
admin.site.register(ImageProduct)
admin.site.register(BrandProduct)

