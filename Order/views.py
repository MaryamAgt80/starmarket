from django.shortcuts import render
from .models import Address, DetilOrder, Order
from Accounts.models import User
from Product.models import Product, DetailProduct, Phone, System
from django.views import View
from django.http import HttpRequest, JsonResponse
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# Create your views here.
@method_decorator(login_required(login_url='login'), name='dispatch')
class ShowCartPage(View):
    def get(self, request: HttpRequest):
        OrderUser, state = Order.objects.get_or_create(user_id=request.user.id, status=0)
        detail_orders = OrderUser.ordermain.all()
        checkdetail_order(request)
        detail_orders = OrderUser.ordermain.all()
        address = ''
        status = True
        if detail_orders.count() > 0:
            address = Address.objects.filter(user_id=request.user.id).order_by('-id')
        else:
            status = False
        price_products = OrderUser.all_price()
        price_post = price_products + 30000
        return render(request, 'pages/cart.html',
                      {'DetailOrder': detail_orders, 'Address': address, 'price_post': price_post,
                       'price_prodducts': price_products, 'status': status})


@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteCart(View):
    def get(self, request: HttpRequest, id):
        status = True
        try:
            detail_order: DetilOrder = DetilOrder.objects.filter(order_main__user_id=request.user.id, id=id).first()
            detail_order.delete()
        except:
            status = False
        return JsonResponse({'status': status})


@method_decorator(login_required(login_url='login'), name='dispatch')
class Change_Count(View):
    def get(self, request: HttpRequest):
        status = False
        message = ''
        try:
            id = int(request.GET.get('id'))
            verb = request.GET.get('verb')
            order_detail = DetilOrder.objects.filter(order_main__user_id=request.user.id, id=id).first()
            if order_detail.detail_product.product.name_class == 'Pooshak':
                if verb == 'plus':
                    order_detail.count += 1
                    if order_detail.count <= order_detail.detail_pooshak.count:
                        order_detail.save()

                        status = True
                    else:
                        message = 'عدم موجودی انبار'
                else:
                    order_detail.count -= 1
                    status = True
                    order_detail.save()
            else:
                if verb == 'plus':
                    order_detail.count += 1
                    if order_detail.count <= order_detail.detail_product.count:
                        order_detail.save()
                        status = True

                    else:
                        message = 'عدم موجودی انبار'
                else:
                    order_detail.count -= 1
                    status = True
                    order_detail.save()
        except:
            pass
        return JsonResponse({'status': status, 'message': message})


@login_required(login_url='login')
def checkdetail_order(request: HttpRequest):
    MainOrder: Order = Order.objects.filter(user_id=request.user.id, status=0).first()
    if MainOrder is not None:
        details_order = MainOrder.ordermain.all()
        for detail in details_order:
            if detail.detail_product.product.name_class == 'Pooshak':
                if detail.detail_pooshak.count < detail.count:
                    detail.delete()
            else:
                if detail.detail_product.count < detail.count:
                    detail.delete()
        MainOrder.save()
