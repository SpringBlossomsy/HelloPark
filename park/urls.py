from django.conf.urls import url
from park import views
from django.views.generic.base import TemplateView


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^send_message/$', views.send_message, name='send_message'),
    url(r'^send_message2/$', views.send_message2, name='send_message2'),
    url(r'^login/$', views.my_login, name='login'),
    url(r'^login_yz/$', views.my_login_yz, name='login_yz'),
    url(r'^logout/$', views.my_logout, name='logout'),
    url(r'^register/$', views.my_register, name='register'),

    url(r'^setSei/$', views.setSei, name='setSei'),
    url(r'^center/$', views.center, name='center'),

    url(r'^add_park/$',views.add_park, name='add_park'),
    url(r'^add_park_inform/$', views.add_park_inform, name='add_park_inform'),




    url(r'^bai_du_map/$', views.bai_du_map, name='bai_du_map'),

    url(r'^test/$', views.test, name='test'),
]
