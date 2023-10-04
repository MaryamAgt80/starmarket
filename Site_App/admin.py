from django.contrib import admin
from .models import Article,ArticleCategory,About_Us,Contact_Us,MessageToAdmin,Slider,AdminToUser,Site_scrape
# Register your models here.
admin.site.register(Article)
admin.site.register(ArticleCategory)
admin.site.register(About_Us)
admin.site.register(Contact_Us)
admin.site.register(MessageToAdmin)
admin.site.register(Slider)
admin.site.register(AdminToUser)
admin.site.register(Site_scrape)