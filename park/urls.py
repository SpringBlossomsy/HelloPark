from django.conf.urls import url
from park import views
from django.views.generic.base import TemplateView


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^setSei/$', views.setSei, name='setSei'),
    url(r'^center/$', views.center, name='center'),
    # 登录/注册
    url(r'^send_message/$', views.send_message, name='send_message'),
    url(r'^send_message2/$', views.send_message2, name='send_message2'),
    url(r'^login/$', views.my_login, name='login'),
    url(r'^login_yz/$', views.my_login_yz, name='login_yz'),
    url(r'^logout/$', views.my_logout, name='logout'),
    url(r'^register/$', views.my_register, name='register'),
    # 钱包
    url(r'^wallet/$', views.my_wallet, name='wallet'),
    url(r'^wallet_invest/$', views.my_wallet_invest, name='wallet_invest'),
    url(r'^wallet_pay/(?P<number>.+)/$', views.my_wallet_pay, name='wallet_pay'),
    url(r'^ddpay/$', views.ddpay, name='ddpay'),
    url(r'^wallet_datail/$', views.my_wallet_datail, name='wallet_datail'),
    url(r'^wallet_datail_more/(?P<walletId>.+)/$', views.my_wallet_datail_more, name='wallet_datail_more'),
    # 我的车辆
    url(r'^car_bind/$', views.car_bind, name='car_bind'),
    url(r'^car_number/$', views.car_number, name='car_number'),
    url(r'^car_save/$', views.car_save, name='car_save'),
    url(r'^car_delete/$', views.car_delete, name='car_delete'),
    # 停车位
    url(r'^park/$', views.park, name='park'),
    url(r'^park_detail/(?P<parkId>.+)/$', views.park_detail, name='park_detail'),
    url(r'^park_change/$', views.park_change, name='park_change'),
    url(r'^add_park/$',views.add_park, name='add_park'),
    url(r'^add_park_inform/$', views.add_park_inform, name='add_park_inform'),
    url(r'^park_save/$', views.park_save, name='park_save'),
    url(r'^park_check/$', views.park_check, name='park_check'),
    # 主功能-停车
    url(r'^park_info/(?P<parkId>.+)/$', views.park_info, name='park_info'),
    url(r'^put_order/$', views.put_order, name='put_order'),
    url(r'^cancel_order/$', views.cancel_order, name='cancel_order'),
    url(r'^self_lock/(?P<parkId>.+)/$', views.self_lock, name='self_lock'),  # 车位主人 使用
    url(r'^self_lock_lock/(?P<parkId>.+)/$', views.self_lock_lock, name='self_lock_lock'),
    url(r'^self_lock_unlock/(?P<parkId>.+)/$', views.self_lock_unlock, name='self_lock_unlock'),
    url(r'^lock/(?P<parkId>.+)/(?P<orderId>.+)/$', views.lock, name='lock'),  # 停车的人使用
    url(r'^lock_start/&', views.lock_start, name='lock_start'),
    url(r'^lock_stop/&', views.lock_stop, name='lock_stop'),
    # 订单
    url(r'^order/$', views.order, name='order'),

    url(r'^test/$', views.test, name='test'),
]
