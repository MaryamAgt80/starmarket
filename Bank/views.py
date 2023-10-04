from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse,Http404,HttpRequest
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
import logging
from Order.models import Address, Order,DetilOrder
from django.apps import apps
from django.shortcuts import redirect
from Order.views import checkdetail_order
post_price=30000
##########################################
@login_required(login_url='LoginAccount')
def go_to_gateway_view(request:HttpRequest,id):
    MainOrderPay:Order=Order.objects.filter(user_id=request.user.id,status=0).first()
    address_first:Address=Address.objects.filter(user_id=request.user.id).first()
    if address_first:
        MainOrderPay.address=address_first
    else:
        redirect('')
        ######### redirect to address
    address = Address.objects.filter(user_id=request.user.id, id=id).first()
    if address is not None:
        MainOrderPay.address.id=id
    MainOrderPay.save()
    ############check detail
    checkdetail_order(request)
    amount=MainOrderPay.all_price()+post_price
    factory = bankfactories.BankFactory()
    bank = factory.create()
    bank.set_request(request)
    bank.set_amount(amount)
    bank.set_client_callback_url(reverse("verify"))
    bank_record = bank.ready()
    return bank.redirect_gateway()

@login_required(login_url='LoginAccount')
def callback_gateway_view(request:HttpRequest):
    MainOrderPay=Order.objects.filter(user_id=request.user.id,status=0).first()
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        # logging.debug("این لینک معتبر نیست.")
        # raise Http404
        return HttpResponse("این لینک معتبر نیست.")

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
         return HttpResponse("این لینک معتبر نیست.")

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
        # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
        #Remove
        Decrisable_count(request)
        MainOrderPay.status=1
        MainOrderPay.save()
        return HttpResponse("پرداخت با موفقیت انجام شد.")

    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    return HttpResponse("پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")

@login_required(login_url='login')
def Decrisable_count(request:HttpRequest):
    MainOrder: Order = Order.objects.filter(user_id=request.user.id, status=0).first()
    if MainOrder is not None:
        details_order = MainOrder.ordermain.all()
        for detail in details_order:
            if detail.detail_product.product.name_class == 'Pooshak':
                detail.detail_pooshak.count -= detail.count
                detail.detail_pooshak.save()
            else:
                detail.detail_product.count -= detail.count
                detail.detail_product.save()