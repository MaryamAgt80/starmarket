from django.urls import path
from . import views

urlpatterns = [
    path('forgot_pass_active/<str:pk>', views.ForgotPass.as_view(),name='forgot_pass_active'),
    path('active_email/<str:code>', views.Active_Email,name='acticve_email'),
    path('active-account/<str:pk>', views.ActiveAccount,name='active-account'),
    path('sign/', views.RcordUser.as_view(),name='sign'),
    path('login/', views.LogUser.as_view(),name='login'),
    path('logout/', views.LogOut,name='logout'),
    path('panel-account/', views.PanelAccount,name='panel-account'),
    path('panel-admin/', views.panel_admin,name='panel-admin'),
    path('change_pass/', views.ChangePass.as_view(),name='change_pass'),
    path('edit_profile/', views.EditProfile.as_view(),name='edit_profile'),
    path('edit_email/', views.EditEmail.as_view(),name='edit_email'),
    path('add_address', views.AddAddress.as_view(), name='add_address'),
    path('editcity', views.Show_Cities),
    path('edit_address/editcity', views.Show_Cities),
    path('address_page', views.AllAddress,name='address_page'),
    path('remove_address', views.RemoveAddres),
    path('edit_address/<int:id>', views.EditAddress.as_view(),name='edit_address'),
    path('forgot_pass', views.send_email_pass.as_view(),name='forgot_pass'),
    path('massege', views.CommentToAdmin,name='massege_admin'),
    path('comment/single/<int:id>', views.CommentSingleAdmin.as_view()),
    path('massege/delete', views.chango_to_ready),
    path('comment/single/massege/delete', views.chango_to_ready),




]
