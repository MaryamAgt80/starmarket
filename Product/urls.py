from django.urls import path,include
from . import views
urlpatterns=[
    path('',views.IndexPage,name='ShowFirstPage'),
    path('products',views.ShowAllProduct.as_view(),name='products'),
    path('brands/<str:brand>',views.ShowBrand.as_view(),name='brand'),
    path('detail/<int:id>',views.DetailProductClass.as_view(),name='detail'),
    path('like/<int:id>',views.checklike.as_view(),name='like'),
    path('like_list/',views.LikeProducts.as_view(),name='like_list'),
    path('new_comment/',views.NewComment.as_view(),name='new_comment'),
    path('cate/<str:cate>',views.ShowProductCategorize.as_view(),name='categorize'),
    path('search/<str:search>',views.ShowSearchProducts.as_view(),name='search'),

]