import datetime

from django.db import models
from Accounts.models import User
from django.core.validators import MinLengthValidator

class Contact_Us(models.Model):
    name_gap=models.CharField(max_length=200,verbose_name='اسم گروه')
    anable=models.BooleanField(default=True,verbose_name='فعال/غیر فعال')
    address_contact=models.CharField(max_length=100,verbose_name='ادرس :کشور-استان-شهر')
    address_detail=models.CharField(max_length=100,null=True,blank=True,default=True,verbose_name='جزئیات ادرس')
    email=models.CharField(max_length=300,verbose_name='ایمیل')
    fax=models.CharField(max_length=11,validators=[MinLengthValidator(11)],verbose_name='فکس')
    phone_number=models.CharField(max_length=11,validators=[MinLengthValidator(11)],verbose_name='شماره تلفن')
    id_insta=models.URLField(verbose_name='لینک اینستا')
    id_soroosh=models.URLField(verbose_name='لینک سروش')
    id_bale=models.URLField(verbose_name='لینک بله')
    image_address=models.ImageField(upload_to='contact_us',verbose_name='تصویر')
    class Meta:
        verbose_name_plural = 'اطلاعات تماس با ما'
        verbose_name = 'اطلاعات'

    def __str__(self):
        return f"{self.name_gap}"

class About_Us(models.Model):
    enable=models.BooleanField(default=True,verbose_name='فعال / غیر فعال')
    about_us=models.TextField(verbose_name='درباره ما')
    logo=models.ImageField(upload_to='contact_us',blank=True,verbose_name='logo')
    class Meta:
        verbose_name_plural = 'درباره ی ما'
        verbose_name = 'درباره ما'


class MessageToAdmin(models.Model):
    name=models.CharField(max_length=200,verbose_name='نام')
    title=models.CharField(max_length=200,verbose_name='عنوان')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_contact',verbose_name='کاربر')
    message = models.TextField(verbose_name='پیغام')
    is_ready=models.BooleanField(default=False,verbose_name='خوانده شده/نشده',null=True,blank=True)
    class Meta:
        verbose_name_plural = 'پیام ها'
        verbose_name = 'پیام'

    def __str__(self):
        return f"{self.title}--{self.user.name}"
class ArticleCategory(models.Model):
    parent = models.ForeignKey('ArticleCategory', null=True, blank=True, on_delete=models.CASCADE,
                               verbose_name='دسته بندی والد')
    title = models.CharField(max_length=200, verbose_name='عنوان دسته بندی')
    url_title = models.CharField(max_length=200, unique=True
                                 , verbose_name='عنوان در url')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی مقاله'
        verbose_name_plural = 'دسته بندی های مقاله'


class Article(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان مقاله')
    slug = models.SlugField(max_length=400, db_index=True, allow_unicode=True, verbose_name='عنوان در url')
    image = models.ImageField(upload_to='contact_us', verbose_name='تصویر مقاله')
    short_description = models.TextField(verbose_name='توضیحات کوتاه')
    text = models.TextField(verbose_name='متن مقاله')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    selected_categories = models.ManyToManyField(ArticleCategory, verbose_name='دسته بندی ها',related_name='categorize')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'مقالات'
class Slider(models.Model):
    image=models.ImageField(upload_to='Slider')
    url_slider=models.URLField()
    in_active=models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = 'اسلایدرها'
        verbose_name = 'اسلایدر'

    def __str__(self):
        return f"{self.url_slider}"

class AdminToUser(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_message',verbose_name='کاربر')
    message=models.TextField(verbose_name='پاسخ')
    admin_po=models.ForeignKey(User,on_delete=models.CASCADE,related_name='admin_massege',verbose_name='ادمین')
    message_user=models.ForeignKey(MessageToAdmin,on_delete=models.CASCADE,default='',blank=True,null=True,verbose_name='پیام کاربر')
    def __str__(self):
        return self.user.name
    class Meta:
        verbose_name_plural='پاسخ ها'
        verbose_name='پاسخ'

#class of scrape other sites
class Site_scrape(models.Model):
    name=models.CharField(max_length=100,verbose_name='نام')
    address_element=models.CharField(max_length=200,verbose_name='ادرس المنت')
    image=models.ImageField(upload_to='images_site',verbose_name='تصویر')
    type=models.IntegerField(verbose_name='روش جستوجو')
    type_search=models.IntegerField(default=0,verbose_name='نوع خراش')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural='اطلاعات سایت های دیگر'
        verbose_name='اطلاعات سایت های دیگر'
