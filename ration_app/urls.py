"""e_ration_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    
   # path('admin/', admin.site.urls),
    
   path('',views.index,name='index'),
   path('index/',views.index,name='index'),
   
   # user views
   
   path('user_register/',views.user_register,name='user_register'),
   path('user_login/',views.user_login,name='user_login'),
   path('user_profile/',views.user_profile,name='user_profile'),
   path('user_home/',views.user_home,name='user_home'),
   
   # shop owner views
   
   path('shop_register/',views.shop_register,name='shop_register'),
   path('shop_login/',views.shop_login,name='shop_login'),
   path('shop_profile',views.shop_profile,name='shop_profile'),
   path('shop_home',views.shop_home,name='shop_home'),
   
   path('add_shop/',views.add_shop,name='add_shop'),
   path('add_pro/',views.add_pro,name='add_pro'),
   path('feedback/',views.feedback,name='feedback'),
   
   path('shops_view',views.shops_view,name='shops_view'),
   path('pro_view/<int:id>',views.pro_view,name='pro_view'),
   
   path('edit_profile',views.edit_profile,name='edit_profile'),
   path('update_profile/',views.update_profile,name='update_profile'),
   
   # cart views
   
    path('addtocart/<int:id>/', views.addtocart, name='addtocart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('error/', views.error, name='error'),
   
   
#    path('my_cart/',views.my_cart,name='my_cart'),
   path('delete_record/<int:id>',views.delete_record,name="delete_record"),
   path('view_orders/',views.view_orders,name='view_orders'),
   path('pay_history/',views.pay_history,name='pay_history'),
   
   # payment urls
   
   path('buy/', views.buy_product, name='buy_product'),
   path('payment_success/', views.payment_success, name='payment_success'),
   
   # admin views
   
   path('admin_reg/',views.admin_reg,name='admin_reg'),
   path('admin_login/',views.admin_login,name='admin_login'),
   path('admin_home/',views.admin_home,name='admin_home'),
   
   path('users_list/',views.users_list,name='uers_list'),
   path('delete_record1/<int:id>',views.delete_record1,name="delete_record1"),

   path('owners_list/',views.owners_list,name='owners_list'),
   path('delete_record2/<int:id>',views.delete_record2,name="delete_record2"),
   
   path('pay_list/',views.pay_list,name='pay_list'),
   path('delete_record3/<int:id>',views.delete_record3,name="delete_record3"),
   
   path('feed_list/',views.feed_list,name='feed_list'),
   path('delete_record4/<int:id>',views.delete_record4,name="delete_record4"),


    # edit product
    path('edit_product/<int:id>',views.edit_product,name='edit_product'),
    path('update_product/',views.update_product,name='update_product'),  
]


