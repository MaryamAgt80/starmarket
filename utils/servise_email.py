from django.core.mail import send_mail,send_mass_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from starmarket import settings
def send_email_text(subject,to,context,template_name):
    HostEmail=settings.EMAIL_HOST_USER
    print(HostEmail)
    html_page=render_to_string(template_name,context)
    end_page=strip_tags(html_page)
    print(to)
    try:
        send_mail(subject,end_page,HostEmail,[to],html_message=html_page)
    except:
        print('gggggggggggggggggggggggg')