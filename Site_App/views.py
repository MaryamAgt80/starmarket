from django.shortcuts import render
from django.views import View
from django.http import HttpRequest
from .forms import MessageForm
from .models import Contact_Us, ArticleCategory, MessageToAdmin, About_Us
import time
from django.http import HttpRequest, JsonResponse
from Site_App.models import Site_scrape
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from requests_html import HTMLSession


class ContactUs(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            form = MessageForm()
        else:
            form = 'برای فرستادن پیام خود ابتدا وارد سایت شوید!'
        contact_info: Contact_Us = Contact_Us.objects.filter(anable=True).first()
        return render(request, 'pages/contact-us.html', {'form': form, 'Contact_Info': contact_info})

    def post(self, request: HttpRequest):
        form = MessageForm(request.POST)
        state = False
        status = ''
        contact_info: Contact_Us = Contact_Us.objects.filter(anable=True).first()
        if form.is_valid():
            if request.user.is_authenticated:
                mesage_contact = MessageToAdmin.objects.create(name=form.cleaned_data.get('name'),
                                                               title=form.cleaned_data.get('title'),
                                                               message=form.cleaned_data.get('message'),
                                                               user_id=request.user.id)
                mesage_contact.save()
                status = 'پیام شما با موفقیت ارسال شد'
                state = True

            else:
                status = 'برای ارسال پیام لطفا لاگین کنید'
        return render(request, 'pages/contact-us.html',
                      {'form': form, 'Contact_Info': contact_info, 'state': state, 'status': status})


def panel_footer(request):
    Categorises = ArticleCategory.objects.filter(is_active=True)
    About = About_Us.objects.filter(enable=True).last()
    return render(request, 'base/footer.html', {'Categorises': Categorises, 'About': About})


def AboutUs(request):
    about: About_Us = About_Us.objects.filter(enable=True).last()
    contact: Contact_Us = Contact_Us.objects.filter(anable=True).last()
    return render(request, 'pages/About.html', {'Contact': contact, 'About': about})


