from django.db import models
from Accounts.models import User
from Product.models import Product, DetailProduct,DetailPooshak
from django.core.validators import MinLengthValidator,MinValueValidator,MaxValueValidator

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='useraddress',verbose_name='کاربر')
    state = models.CharField(max_length=100,verbose_name='استان')
    city = models.CharField(max_length=100,verbose_name='شهر')
    address = models.TextField(verbose_name='آدرس')
    post_code = models.CharField(max_length=9,validators=[MinLengthValidator(9)],blank=True,verbose_name='کد پستی')
    class Meta:
        verbose_name_plural='آدرس ها'
        verbose_name='آدرس'
    def __str__(self):
        return f'{self.user.name} {self.state}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userorder',verbose_name='کاربر')
    list_status = ((0, 'پرداخت نشده'), (1, 'پرداخت شده'), (2, 'مرجوع شده'))
    status = models.IntegerField( choices=list_status, default=0,verbose_name='وضعیت')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='orderaddres', null=True,verbose_name='ادرس')
    created_date = models.DateField(auto_now=True,verbose_name='تاریخ ایجاد')
    TrackingCode=models.CharField(max_length=200,default='',null=True,blank=True)

    class Meta:
        verbose_name_plural='سبد های خرید'
        verbose_name='سبد خرید'

    def all_price(self):
        details=self.ordermain.all()
        all_price=0
        for detail in details:
            all_price+=detail.detail_product.product.price*detail.count
        return all_price


class DetilOrder(models.Model):
    detail_product = models.ForeignKey(DetailProduct, on_delete=models.CASCADE,null=True,blank=True,verbose_name='جزئیات محصول')
    detail_pooshak=models.ForeignKey(DetailPooshak,on_delete=models.CASCADE,blank=True,default='',null=True,verbose_name='جزئیات پوشاک')
    count = models.IntegerField(verbose_name="تعداد")
    order_main = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='ordermain',verbose_name='سبد خرید اصلی')
    def return_price(self):
        return self.detail_product.product.price * self.count
    class Meta:
        verbose_name_plural='جزِئیات سفارشات'
        verbose_name='چزئیات سفارش'
    def __str__(self):
        return self.detail_product.product.name

class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_like',verbose_name='کاربر')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_like',verbose_name='محصول')
    class Meta:
        verbose_name_plural='محصولات پسندیده شده'
        verbose_name='محصول پسندیده شده'
    def __str__(self):
        return f"{self.product.id} {self.product.name}"




