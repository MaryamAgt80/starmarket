"""starmarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from azbankgateways.urls import az_bank_gateways_urls

admin.autodiscover()
from Bank import views

urlpatterns = [
    path('admin/', admin.site.urls,name='admin_django'),
    path('bankgateways/', az_bank_gateways_urls()),
    path('accounts/', include('Accounts.urls')),
    path('cart/', include('Order.urls')),
    path('paymoney/<int:id>', views.go_to_gateway_view, name='paymony'),
    path('verify', views.callback_gateway_view, name='verify'),
    path('contact/', include('Site_App.urls')),
    path('scrape/', include('selenium_app.urls')),
    path('', include('Product.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
