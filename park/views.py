from django.shortcuts import render
from registration.backends.simple.views import RegistrationView
import re
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import *
from django.urls import reverse
from django.contrib.auth.models import User, Group
from park.forms import *
from park.models import *
from json import *
import datetime
import time
import os
from django.db.models import Q
from django.conf import settings
import random
import urllib
import http.client


key = 'w1PFgbVb9cHY25GajgfS2chYFKH0inev'



class MyRegistrationView(RegistrationView):  # 用户成功注册后重定向到其他页面
    def get_success_url(self, user):
        return reverse('index', user.username)


def index(request):
    return render(request, 'base.html')


# -----------------发送短信的视图函数---------------------------------------------------------------
# 请求的路径
host = "106.ihuyi.com"
sms_send_uri = "/webservice/sms.php?method=Submit"
# 用户名是登录ihuyi.com账号名（例如：cf_demo123）
account = "C03611718"
# 密码 查看密码请登录用户中心->验证码、通知短信->帐户及签名设置->APIKEY
password = "8610a2971e9856ab4f62e2d9a06915b6"


def message(request, mobile):
    # 定义一个字符串,存储生成的6位数验证码
    message_code = ''
    for i in range(6):
        i = random.randint(0, 9)
        message_code += str(i)
    # 拼接成发出的短信
    text = "您的验证码是：" + message_code + "。请不要把验证码泄露给其他人。"
    # 把请求参数编码
    params = urllib.parse.urlencode(
        {'account': account, 'password': password, 'content': text, 'mobile': mobile, 'format': 'json'})
    # 请求头
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    # 通过全局的host去连接服务器
    conn = http.client.HTTPConnection(host, port=80, timeout=30)
    # 向连接后的服务器发送post请求,路径sms_send_uri是全局变量,参数,请求头
    conn.request("POST", sms_send_uri, params, headers)
    # 得到服务器的响应
    response = conn.getresponse()
    # 获取响应的数据
    response_str = response.read()
    # 关闭连接
    conn.close()
    # 把验证码放进session中
    request.session['message_code'] = message_code
    # print(eval(response_str.decode()))
    # 使用eval把字符串转为json数据返回
    return JsonResponse(eval(response_str.decode()))


def send_message(request):
    """发送信息的视图函数"""
    # 获取ajax的get方法发送过来的手机号码
    mobile = request.GET.get('mobile')
    # 通过手机去查找用户是否已经注册
    user = User.objects.filter(username=mobile)
    if len(user) == 1:
        return JsonResponse({'msg': "该手机已经注册"})
    return message(request, mobile)


def send_message2(request):
    """发送信息的视图函数"""
    # 获取ajax的get方法发送过来的手机号码
    mobile = request.GET.get('mobile')
    # 通过手机去查找用户是否已经注册
    user = User.objects.filter(username=mobile)
    if len(user) == 0:
        return JsonResponse({'msg': "该手机尚未注册"})
    return message(request, mobile)

# ----------------登录--------------------------------------------------------------------------
def my_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'login_register.html')


def my_login_yz(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        code = request.POST.get("code", "")
        if code == request.session['message_code']:
            user = User.objects.get(username=username)
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'login_register.html')


def my_logout(request):
    logout(request)
    return redirect('index')


# ----------------注册--------------------------------------------------------------------------
def my_register(request):
    if request.method == 'POST':
        if request.POST.get('code') == request.session['message_code']:
            u = User.objects.create_user(username=request.POST.get('mobile'), password=request.POST.get('password'))
            u.save()
            up = UserProfile.objects.get_or_create(user=u)
            up.save()
            return HttpResponse('注册成功')
    return render(request, 'login_register.html')


# --------------------- 百度地图---------------------------------------------------------------
def bai_du_map(request):
    return render(request, 'bai_du_map.html')


def parking_space_submit(request):
    return render(request, 'parking_space_submit.html')


def parking_space_location(request):
    return render(request, 'parking_space_location.html')


# ----------------qita-------------------------------------------------------------------------
def test(request):
    return render(request, 'test.html', {'key': key})


