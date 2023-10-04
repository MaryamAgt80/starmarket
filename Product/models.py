from django.db import models
from Accounts.models import User
from  datetime import datetime
#######################################################
class BrandProduct(models.Model):
    brand=models.CharField(max_length=100,verbose_name='برند')
    url_field=models.CharField(max_length=100,verbose_name='عنوان برند')
    image_field=models.ImageField(upload_to='image_brand',blank=True,default=True,verbose_name='عکس برند')
    class Meta:
        verbose_name_plural = 'برند ها'
        verbose_name = 'برند'


    def __str__(self):
        return self.brand
class Categorize_Products(models.Model):
    title=models.CharField(max_length=100,verbose_name='عنوان دسته بندی')
    parent=models.ForeignKey('Categorize_Products',on_delete=models.CASCADE,null=True,blank=True,related_name='subset',verbose_name='زیر مجموعه:')
    cate_name=models.CharField(max_length=100,verbose_name='نام دسته بندی')
    is_active=models.BooleanField(default=True,verbose_name='فعال/غیر فعال')
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = 'دسته بندی های محصولات'
        verbose_name = 'دسته بندی محصول'



############################ Product ####################################3
class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام محصول')
    price = models.IntegerField(verbose_name="قیمت")
    count_like = models.IntegerField(verbose_name="تعداد لایک", default=0)
    offer_price = models.IntegerField(verbose_name='تخفیف', default=0)
    count_buy = models.IntegerField(default=0,verbose_name='تعداد فروش')
    brand_p=models.ForeignKey(BrandProduct,on_delete=models.CASCADE,related_name='brand_product',default='',blank=True,null=True,verbose_name='برند')
    categorizes=Categorize_Products.objects.all()
    list_cate = []
    for cate in categorizes:
        list_cate.append((cate.cate_name,cate.title))
    list_cate=tuple(list_cate)

    categorize = models.CharField(max_length=20, choices=list_cate, default='Digital',verbose_name='دسته بندی')
    list_class = (('Pooshak', 'پوشاک'),
                  ('Phone', 'موبایل'),
                  ('System', 'سیستم'),
                  ('TV', 'تلوزیون'),
                  ('Laundry', 'لبتسشویی'),
                  ('Refrigerator', 'یخچال'),
                  ('Headset', 'هندزفری و ایر پاد'),
                  ('Bag','کیف و کاور لپ تاپ'),
                  ('Cover','کاور گوشی'),
                  ('Oven','اجاق'),
                  )
    name_class = models.CharField(max_length=30, choices=list_class, default='System', verbose_name='نام کلاس')
    class Meta:
        verbose_name_plural = ' محصولات'
        verbose_name = ' محصول'

    def __str__(self):
        return self.name
    def CountAll(self):
        count=0
        if self.name_class=='Pooshak':
            for detail_product in self.ProductMain.all():
                detail_product.CountPooshak()
                count+=detail_product.count
        else:
            for detail_product in self.ProductMain.all():
                count+=detail_product.count
        return count
#########################
class ImageProduct(models.Model):
    image=models.ImageField(upload_to='image_product',verbose_name='عکس')
    product_image=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='AutherImage',verbose_name='محصول')
    class Meta:
        verbose_name_plural = 'تصاویر محصولات'
        verbose_name = 'تصویر محصول'

    def __str__(self):
        return f"{self.product_image.product.name}"
####################################################
class ImageCategorize(models.Model):
    cate_image=models.ForeignKey(Categorize_Products,on_delete=models.CASCADE,related_name='imagecate',verbose_name='دسته بندی')
    image=models.ImageField(upload_to='image_cate',default='',verbose_name='عکس')
    class Meta:
        verbose_name_plural = 'تصاویر دسته بندی ها'
        verbose_name = 'تصویر دسته بندی'

    def __str__(self):
        return f"{self.cate_image.cate_name}"
######################################################
class Comment(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product',verbose_name='محصول')
    massege=models.TextField(verbose_name='پبام')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user',verbose_name='کاربر')
    name=models.CharField(max_length=200,verbose_name='نام')
    lname=models.CharField(max_length=200,default='',blank=True,verbose_name='فامیلی')
    date=models.DateField(auto_now=True,verbose_name='تاریخ')
    time=models.TimeField(auto_now=True,verbose_name='زمان ثبت')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'نظرات'
        verbose_name = 'نظر'


############################## DetailProduct #######################

class DetailProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ProductMain',
                                verbose_name='محصول مربوطه')
    image = models.ImageField(upload_to='ProductImages', verbose_name='عکس محصول', default='', null=True)
    color_code = models.CharField(max_length=20, verbose_name= "کد رنگ")
    count = models.IntegerField(null=True,verbose_name='تعداد')
    def CountPooshak(self):
        if self.product.name_class=='Pooshak':
            self.count=0
            for detail_pooshak in self.detail_pooshak.all():
                self.count+=detail_pooshak.count
            self.save()
    class Meta:
        verbose_name_plural = 'جزئیات محصولات'
        verbose_name = 'جزئیات محصول'

    def __str__(self):
        return f"{self.product.name} {self.color_code}"



class System(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name="محصول مربوطه")
    processor_seri = models.CharField(max_length=100, verbose_name='سری پردازنده')
    model = models.CharField(max_length=100, verbose_name='مدل')
    size_screen = models.CharField(max_length=100, verbose_name='اندازه صفحه')
    ram_capacity = models.IntegerField(verbose_name='ظرفیت RAM')
    ram_type = models.CharField(max_length=10, verbose_name='نوع حافظه')
    GPU_manufacture = models.CharField(max_length=100, verbose_name='شرکت سازنده')
    guarantee_time = models.CharField(max_length=100, verbose_name='گارانتی')
    capcity_hard = models.IntegerField(verbose_name='ظرفیت هارد')
    weight = models.CharField(max_length=100, verbose_name='وزن')
    system_func = models.CharField(max_length=100, verbose_name='سیستم عامل')
    number_port = models.IntegerField(default=0, verbose_name='تعداد پورت')
    connect_door = models.CharField(max_length=100, verbose_name='تعداد درگاه ها ارتباطی')
    webcam = models.CharField(max_length=100,default='دارد' ,verbose_name='وبکم')

    class Meta:
        verbose_name_plural = 'سیستم ها'
        verbose_name = 'سیستم'

    def __str__(self):
        return self.product.name


######################### Phone  ####################

class Phone(models.Model):
    product=models.OneToOneField(Product,on_delete=models.CASCADE,verbose_name='محصول مربوططه')
    model=models.CharField(max_length=100,verbose_name='مدل')
    size_screen=models.CharField(max_length=100,verbose_name='انندازه صفحه')
    system_type=models.CharField(max_length=20,verbose_name='نوغ سیستم عامل')
    weight=models.CharField(max_length=20,verbose_name='وزن')
    number_sim=models.IntegerField(verbose_name='تعداد سیم')
    hard=models.IntegerField(verbose_name='ظرفیت هارد')
    ram_number=models.IntegerField(verbose_name='ظرفیت رم')
    resolvation_image=models.CharField(max_length=100,verbose_name='رزولیشن عکس')
    included_items=models.TextField(verbose_name='اقلام همراه')
    screen_technology=models.CharField(max_length=100,verbose_name='تکنولوژی صفحه')
    def __str__(self):
        return f"{self.product.name}"
    class Meta:
        verbose_name_plural = 'گوشی ها'
        verbose_name = 'گوشی'


    ###########################################################
class Pooshak(models.Model):
    product=models.OneToOneField(Product,on_delete=models.CASCADE,verbose_name='محصول اصلی')
    model=models.CharField(max_length=200,verbose_name='مدل',blank=True)
    Maintenance=models.TextField(null=True,verbose_name='شرایط نگهداری',blank=True)
    description=models.TextField(null=True,verbose_name='توضیحات',blank=True)
    sex=models.CharField(max_length=100,default='',verbose_name='جنس')
    class Meta:
        verbose_name_plural = 'لباس ها'
        verbose_name = 'لباس'

    def __str__(self):
        return f"{self.product.name} {self.sex}"

class DetailPooshak(models.Model):
    size=models.CharField(max_length=100,verbose_name='سایز')
    count=models.IntegerField(verbose_name='تعداد')
    detail_product=models.ForeignKey(DetailProduct,on_delete=models.CASCADE,related_name='detail_pooshak',verbose_name='جزئیات محصول')
    class Meta:
        verbose_name_plural = 'جزئیات لباس ها'
        verbose_name = 'جزئیات لباس'

    def __str__(self):
        return f"{self.count}--{self.size}"

####################################################################

class Bag(models.Model):
    product=models.OneToOneField(Product,on_delete=models.CASCADE,verbose_name='محصول مربوطه')
    model=models.CharField(max_length=100,verbose_name='مدل')
    Suitable=models.CharField(max_length=100,verbose_name='مناسب برای')
    weight=models.CharField(max_length=100,verbose_name='وزن')
    description=models.TextField(blank=True,null=True,verbose_name='توضیحات')
    ability=models.TextField(blank=True,null=True,verbose_name='قابلیت')
    class Meta:
        verbose_name_plural = 'کیف ها'
        verbose_name = 'کیف'

    def __str__(self):
        return f"{self.product.name}"
#############################
class Cover(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE,verbose_name='محصول مربوطه')
    model = models.CharField(max_length=100,verbose_name='مدل')
    Suitable = models.CharField(max_length=100,verbose_name='مناسب برای')
    weight = models.CharField(max_length=20,verbose_name='وزن')
    stracture=models.CharField(max_length=20,verbose_name='ساختار')
    description = models.TextField(blank=True, null=True,verbose_name='توضیحات')
    Surface_coverage = models.TextField(blank=True, null=True,verbose_name='پوشش سطح')
    Ability=models.TextField(blank=True,verbose_name='قابلیت ')
    class Meta:
        verbose_name_plural = 'کاورها'
        verbose_name = 'کاور'

    def __str__(self):
        return f"{self.product.name}"
########################################
class Refrigerator(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE,verbose_name='محصول مربوطه')
    model = models.CharField(max_length=100,verbose_name='مدل')
    foot = models.CharField(max_length=20,verbose_name='فوت')
    type=models.CharField(max_length=20,verbose_name='نوع یخچال')
    chart_energy=models.CharField(max_length=1,verbose_name='نمودار انرژی')
    type_translate_barfak=models.CharField(max_length=100,verbose_name='نوع مقاومت در برابر برفک')
    weight = models.CharField(max_length=20,verbose_name='وزن')
    height=models.CharField(max_length=20,verbose_name='ارتفاع')
    v_Refrigerator=models.CharField(max_length=20,verbose_name='گنجایش به یخچال')
    V_freeze=models.CharField(max_length=20,verbose_name='گنجایش به فریز')
    v_all_to_foot=models.CharField(max_length=20,verbose_name='گنجایش کل به فوت')
    v_all_to_litr=models.CharField(max_length=20,verbose_name='گنجایش کل به لیتر')
    h=models.CharField(max_length=20,verbose_name='عمق')
    width=models.CharField(max_length=20,blank=True,default=True,verbose_name='پهنا')
    n_door=models.IntegerField(verbose_name='تعداد در')
    n_floor=models.IntegerField(verbose_name="تعداد طبقه")
    productshenas=models.CharField(max_length=100,verbose_name='شناسه محصول')
    class Meta:
        verbose_name_plural = 'یخچال ها'
        verbose_name = 'یخچال'

    def __str__(self):
        return f"{self.product.name}"
#####################################################
class TV(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE,verbose_name='محصول مربوطه')
    model=models.CharField(max_length=100,verbose_name='مدل')
    quaity_image=models.CharField(max_length=100,verbose_name='کیفیت تصویر')
    resolvation=models.CharField(max_length=100,verbose_name='رزولویشن عکس')
    size=models.FloatField(verbose_name='اندازه صفحه')
    speaker_power=models.CharField(max_length=100,verbose_name='توان بلندگو')
    Aspect_ratio=models.CharField(max_length=100,verbose_name='نسبت تصویر')
    source_energy=models.CharField(max_length=100,verbose_name='منبع انرژی')
    productshenas = models.CharField(max_length=100,verbose_name='شناسه محصول')
    n_usb=models.IntegerField(verbose_name='تعداد usb')
    n_hdmi=models.IntegerField(verbose_name='تعداد hdmi')
    type_screen=models.CharField(max_length=100,verbose_name='نوع صفحه نمایش')
    type_leg=models.CharField(max_length=100,verbose_name='نوع پایه')
    descript=models.CharField(max_length=100,verbose_name='سایر توضیحات')
    productshenas = models.CharField(max_length=100,verbose_name='شناسه محصول')
    class Meta:
        verbose_name_plural = 'تلوزیون ها'
        verbose_name = 'تلوزیون'

    def __str__(self):
        return f"{self.product.name}"
##############################################################################
class Laundry(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE,verbose_name='محصول مربوطه')
    model = models.CharField(max_length=100, verbose_name='مدل')
    kind_sad=models.CharField(max_length=100,verbose_name='نوع مخزن')
    rotation_speed=models.CharField(max_length=100,verbose_name='سرعت چرخش موتور')
    categorize_color=models.CharField(max_length=100,verbose_name='طبقه بندی رنگی')
    capcity=models.CharField(max_length=100,verbose_name='ظرفیت')
    type_motor=models.CharField(max_length=100,verbose_name='نوع موتور')
    h=models.CharField(max_length=100,verbose_name='عمق')
    height=models.CharField(max_length=100,verbose_name='ارتفاع')
    width=models.CharField(max_length=100,verbose_name='پهنا')
    boad=models.CharField(max_length=100,verbose_name='ابعاد')
    productshenas = models.CharField(max_length=100,verbose_name='شناسه محصول')
    class Meta:
        verbose_name_plural = 'لباسشویی ها'
        verbose_name = 'لباسشویی'

    def __str__(self):
        return f"{self.product.name}"
#########################################################
class Oven(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE,verbose_name='محصول مربوطه')
    model = models.CharField(max_length=100, verbose_name='مدل')
    sex_body= models.CharField(max_length=100,verbose_name='جنس بدنه')
    n_flames=models.IntegerField(verbose_name='تعداد شعله')
    place_cooker=models.CharField(max_length=100,verbose_name='مکان شعله پز')
    height = models.CharField(max_length=100,verbose_name='ارتفاع')
    sex_network=models.CharField(max_length=100,verbose_name='جنس شبکه')
    productshenas = models.CharField(max_length=100,verbose_name='شناسه محصول')
    sim_lenght=models.CharField(max_length=100,verbose_name='ظول سیم')
    ability=models.TextField(blank=True,verbose_name='سایر قابلیت ها')
    class Meta:
        verbose_name_plural = 'اجاق گازها'
        verbose_name = 'اجاق گاز'

    def __str__(self):
        return f"{self.product.name}"
###############################################


