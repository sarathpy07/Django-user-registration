from django.conf.urls import url
from passapp import views


app_name = 'passapp'

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^userlogin/$',views. userlogin,name='login'),
]