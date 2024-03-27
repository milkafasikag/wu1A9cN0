# urls.py

from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from django.contrib.auth.views import LogoutView



router = DefaultRouter()
router.register(r'itemtypes', views.ItemListCreateView)
router.register(r'banks', views.BankViewSet, basename='bank')
router.register(r'coupons', views.CouponViewSet, basename='coupon')
router.register(r'order_charts', views.OrderChartViewSet, basename='order_chart')
router.register(r'client', views.ClientViewSet, basename='client')


urlpatterns = [
    # ... other URL patterns ...
    path('', include(router.urls)),
    path('orderview/', views.OrderView.as_view(), name='orderview'),
    path('coupons/<int:pk>/deactivate/', views.CouponViewSet.as_view({'post': 'deactivate'}), name='coupon-deactivate'),
    path('coupons/<int:pk>/activate/', views.CouponViewSet.as_view({'post': 'activate'}), name='coupon-activate'),


    path('register-itemtype/', views.register_item_type, name='register-item-type'),
    path('update_item/<int:id>/', views.update_item_type, name='update_item'),
    path('get_item/<int:item_id>/', views.get_item, name='get-item'),
    path('removeimage/<int:client_id>/<int:itemid>/', views.removeimage, name='removeimage'),
    path('image_add/<int:itemid>/', views.image_add, name='image_add'),


    path('removetext/<int:client_id>/<int:itemid>/', views.removetext, name='removetext'),
    path('textadd/<int:itemid>/', views.text_add, name='text_add'),

    path('shop_order/', views.shop_order, name='shop_order'),

    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('cart_list/', views.cart_list, name='cart_list'),
    path('remove/<int:id>/', views.remove, name='remove'),
    path('discount/', views.discount, name='discount'),
    path('payment_display/<int:id>/', views.payment_display, name='payment_display'),
    path('purchesed_list/', views.purchesed_list, name='purchesed_list'),
    path('client/<int:client_id>/orders/', views.client_orders, name='client_orders'),
    path('PaymentViewSet/<int:client_id>/payment/', views.paymentViewSet, name='PaymentViewSet'),
    path('sendemail/', views.sendemail, name='sendemail'),

    path('payment/<int:payment_id>/upload_receipt/', views.upload_receipt, name='upload_receipt'),



]
