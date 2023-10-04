from django.urls import path
from . import  views
urlpatterns=[
    path('',views.ShowCartPage.as_view(),name='cart'),
    path('deletecart/<int:id>',views.DeleteCart.as_view(),name='delete_cart'),
    path('change_count',views.Change_Count.as_view(),name='change_count'),
    path('check_cart',views.checkdetail_order,name='check_cart'),
]