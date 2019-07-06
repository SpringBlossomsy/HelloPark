from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
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
import json
import datetime
import time
import os
from django.db.models import Q
from django.conf import settings
import random
import urllib
import http.client
from decimal import *


key = 'w1PFgbVb9cHY25GajgfS2chYFKH0inev'



class MyRegistrationView(RegistrationView):  # 用户成功注册后重定向到其他页面
    def get_success_url(self, user):
        return reverse('index')


def index(request):
    us = UserPrakSeat.objects.all()
    ls = []
    print(us)
    for t in us:
        ls.append([t.pioaddress, float(t.lat), float(t.lng), float(t.price), t.id])
        print('***',t)
    print(float(3.14159562))
    return render(request, 'index.html', {'userSeats': ls})


@csrf_exempt
def setSei(request):
    if request.method == 'POST':
        request.session['local_lat'] = request.POST.get('lat')
        request.session['local_lng'] = request.POST.get('lng')
        return HttpResponse("ok")


def center(request):
    return render(request, 'center.html')


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
        try:
            if code == request.session['message_code']:
                user = User.objects.get(username=username)
            if user is not None:
                login(request, user)
                return redirect('index')
        except:
            pass
    return render(request, 'login_register.html')


def my_logout(request):
    logout(request)
    return redirect('index')


# ----------------注册--------------------------------------------------------------------------
def my_register(request):
    if request.method == 'POST':
        if request.POST.get('code') == request.session['message_code']:
            u = User.objects.create_user(username=request.POST.get('mobile'), password=request.POST.get('password'))
            up = UserProfile.objects.get_or_create(user=u)
            return HttpResponse('注册成功')
    return render(request, 'login_register.html')


# ------------------------- 车位---------------------------------------------
@login_required
def park(request):
    s = ''
    try:
        u = UserProfile.objects.get(user=request.user)
        s = UserPrakSeat.objects.filter(user=u)
    except:
        pass
    ls = []
    for t in s:
        temp = [t.pioaddress, t.note, t.price]
        string = ''
        if t.time02 == True:
            string = string + '00:00-02:00,'
        if t.time24 == True:
            string = string + '02:00-04:00,'
        if t.time46 == True:
            string = string + '04:00-06:00,'
        if t.time68 == True:
            string = string + '06:00-08:00,'
        if t.time810 == True:
            string = string + '08:00-10:00,'
        if t.time1012 == True:
            string = string + '10:00-12:00,'
        if t.time1214 == True:
            string = string + '12:00-14:00,'
        if t.time1416 == True:
            string = string + '14:00-16:00,'
        if t.time1618 == True:
            string = string + '16:00-18:00,'
        if t.time1820 == True:
            string = string + '18:00-20:00,'
        if t.time2022 == True:
            string = string + '20:00-22:00,'
        if t.time2224 == True:
            string = string + '22:00-24:00,'
        temp.append(string)
        temp.append(t.id)
        status = ''
        if t.status == '0':
            status = '未通过'
        elif t.status == '1':
            status = '审核通过'
        elif t.status == '2':
            status = '审核中'
        temp.append(status)
        ls.append(temp)

    return render(request, 'My_Park.html', {'seats': ls})


@login_required
def park_detail(request, parkId):
    t = UserPrakSeat.objects.get(id=parkId)
    temp = [t.id, t.pioaddress, t.note, t.price]
    string = ''
    if t.time02 == True:
        string = string + '00:00-02:00,'
    if t.time24 == True:
        string = string + '02:00-04:00,'
    if t.time46 == True:
        string = string + '04:00-06:00,'
    if t.time68 == True:
        string = string + '06:00-08:00,'
    if t.time810 == True:
        string = string + '08:00-10:00,'
    if t.time1012 == True:
        string = string + '10:00-12:00,'
    if t.time1214 == True:
        string = string + '12:00-14:00,'
    if t.time1416 == True:
        string = string + '14:00-16:00,'
    if t.time1618 == True:
        string = string + '16:00-18:00,'
    if t.time1820 == True:
        string = string + '18:00-20:00,'
    if t.time2022 == True:
        string = string + '20:00-22:00,'
    if t.time2224 == True:
        string = string + '22:00-24:00,'
    temp.append(string)
    return render(request, 'My_Park_Detail.html', {'t': temp})


@csrf_exempt
def park_change(request):
    id = request.POST.get('id')
    us = UserPrakSeat.objects.get(id=id)
    us.price = request.POST.get('price')
    # 修改原来的时间
    us.time02 = False
    us.stat02 = False
    us.time24 = False
    us.stat24 = False
    us.time46 = False
    us.stat46 = False
    us.time68 = False
    us.stat68 = False
    us.time810 = False
    us.stat810 = False
    us.time1012 = False
    us.stat1012 = False
    us.time1214 = False
    us.stat1214 = False
    us.time1416 = False
    us.stat1416 = False
    us.time1618 = False
    us.stat1618 = False
    us.time1820 = False
    us.stat1820 = False
    us.time2022 = False
    us.stat2022 = False
    us.time2224 = False
    us.stat2224 = False
    # 添加时间
    choiceTime = request.POST.get('choiceTime').split(',')
    choiceTime = [x[0:2] for x in choiceTime]
    # print(choiceTime)
    for t in choiceTime:
        if t == '00':
            us.time02 = True
            us.stat02 = True
        elif t == '02':
            us.time24 = True
            us.stat24 = True
        elif t == '04':
            us.time46 = True
            us.stat46 = True
        elif t == '06':
            us.time68 = True
            us.stat68 = True
        elif t == '08':
            us.time810 = True
            us.stat810 = True
        elif t == '10':
            us.time1012 = True
            us.stat1012 = True
        elif t == '12':
            us.time1214 = True
            us.stat1214 = True
        elif t == '14':
            us.time1416 = True
            us.stat1416 = True
        elif t == '16':
            us.time1618 = True
            us.stat1618 = True
        elif t == '18':
            us.time1820 = True
            us.stat1820 = True
        elif t == '20':
            us.time2022 = True
            us.stat2022 = True
        elif t == '22':
            us.time2224 = True
            us.stat2224 = True
    us.save()
    return HttpResponse("ok")


@login_required
def add_park(request):
    return render(request, 'My_Park_Add.html')


@csrf_exempt
def add_park_inform(request):
    informations = json.loads(request.POST.get('informations'))
    # print(informations, informations['latlng'])
    lat = informations['latlng']['lat']
    lng = informations['latlng']['lng']
    poiaddress = informations['poiaddress']
    local_lat = request.session.get('local_lat', 29.818722)
    local_lng = request.session.get('local_lng', 121.563897)
    return render(request, 'My_Park_Add_Inform.html', {
        'poiaddress': poiaddress, 'lat': lat, 'lng': lng,
        'local_lat': local_lat, 'local_lng': local_lng
    })


@csrf_exempt
def park_save(request):
    u = UserProfile.objects.get(user=request.user)
    informs = request.POST.get('informs')
    price = request.POST.get('price')
    lat = request.POST.get('lat')
    lng = request.POST.get('lng')
    poiaddress = request.POST.get('poiaddress')
    us = UserPrakSeat.objects.create(user=u, lat=lat, lng=lng, pioaddress=poiaddress,
                                     note=informs, price=int(price), status='2')
    choiceTime = request.POST.get('choiceTime').split(',')
    choiceTime = [x[0:2] for x in choiceTime]
    # print(choiceTime)
    for t in choiceTime:
        if t == '00':
            us.time02 = True
            us.stat02 = True
        elif t == '02':
            us.time24 = True
            us.stat24 = True
        elif t == '04':
            us.time46 = True
            us.stat46 = True
        elif t == '06':
            us.time68 = True
            us.stat68 = True
        elif t == '08':
            us.time810 = True
            us.stat810 = True
        elif t == '10':
            us.time1012 = True
            us.stat1012 = True
        elif t == '12':
            us.time1214 = True
            us.stat1214 = True
        elif t == '14':
            us.time1416 = True
            us.stat1416 = True
        elif t == '16':
            us.time1618 = True
            us.stat1618 = True
        elif t == '18':
            us.time1820 = True
            us.stat1820 = True
        elif t == '20':
            us.time2022 = True
            us.stat2022 = True
        elif t == '22':
            us.time2224 = True
            us.stat2224 = True
    us.save()
    return HttpResponse("ok")


@login_required
def park_check(request):
    return render(request, 'My_Park_Check.html')


# --------------------- 车辆 ---------------------------------------------------------------
@login_required
def car_bind(request):
    u = UserProfile.objects.get(user=request.user)
    card = ''
    if len(u.licence_number) == 7:
        card = u.licence_number
    return render(request, 'My_Car_Bind.html', {'card': card})


@login_required
def car_number(request):
    return render(request, 'My_Car_Number.html')


@login_required
def car_save(request):
    u = UserProfile.objects.get(user=request.user)
    try:
        p = request.GET.get('value')
    except:
        pass
    else:
        if len(p) == 7:
            u.licence_number = p
            u.save()
    return redirect('car_bind')


@login_required
def car_delete(request):
    u = UserProfile.objects.get(user=request.user)
    u.licence_number = ''
    u.save()
    return redirect('car_bind')


# --------------------- 钱包 ---------------------------------------------------------------
@login_required
def my_wallet(request):
    u = UserProfile.objects.get(user=request.user)
    money = u.account
    return render(request, 'My_Wallet.html', {'money': money})


@login_required
def my_wallet_invest(request):
    return render(request, 'My_Wallet_Invest.html')


@login_required
def my_wallet_pay(request, number):
    u = UserProfile.objects.get(user=request.user)
    u.account = float(u.account) + float(int(number))
    u.save()
    w = WalletDetail()
    w.user = u
    w.source = '充值'
    w.price = float(int(number))
    w.status = False
    w.save()
    return redirect('wallet')
    # return render(request, 'My_Wallet_Pay.html')


@login_required
def ddpay(request):
    return render(request, 'ddpay.html')


@login_required
def my_wallet_datail(request):
    details = WalletDetail.objects.filter(user=UserProfile.objects.get(user=request.user))
    return render(request, 'My_Wallet_Detail.html', {'details': details})


@login_required
def my_wallet_datail_more(request, walletId):
    d = WalletDetail.objects.get(id=walletId)
    return render(request, 'My_Wallet_Detail_More.html', {'detail': d})


# --------------------- 主功能：车位详情-生成订单 ---------------------------------------------------------------
@login_required
def park_info(request, parkId):
    up = UserPrakSeat.objects.get(id=parkId)
    time_list = []
    if up.stat02 == True:
        time_list.append('00:00-02:00')
    if up.stat24 == True:
        time_list.append('02:00-04:00')
    if up.stat46 == True:
        time_list.append('04:00-06:00')
    if up.stat68 == True:
        time_list.append('06:00-08:00')
    if up.stat810 == True:
        time_list.append('08:00-10:00')
    if up.stat1012 == True:
        time_list.append('10:00-12:00')
    if up.stat1214 == True:
        time_list.append('12:00-14:00')
    if up.stat1416 == True:
        time_list.append('14:00-16:00')
    if up.stat1618 == True:
        time_list.append('16:00-18:00')
    if up.stat1820 == True:
        time_list.append('18:00-20:00')
    if up.stat2022 == True:
        time_list.append('20:00-22:00')
    if up.stat2224 == True:
        time_list.append('22:00-24:00')
    return render(request, 'Park_Info.html', {'parkinfo': up, 'timeList': time_list})


@csrf_exempt
def put_order(request):
    test = Order.objects.filter(Q(user=UserProfile.objects.get(user=request.user)) &
                                Q(status='0'))
    # 如果存在一个进行中的订单
    if test:
        return redirect('order')
    # 如果余额为负数
    if UserProfile.objects.get(user=request.user).account < 0:
        return redirect('order')
    ls = request.POST.getlist('chongzhi1')
    string = ''
    # 改变 车位的时间锁定
    seat = UserPrakSeat.objects.get(id=request.POST.get('ids'))
    for t in ls:
        string = string + t + ','
        temp = t[:2]
        if temp == '00':
            seat.stat02 = False
        elif temp == '02':
            seat.stat24 = False
        elif temp == '04':
            seat.stat46 = False
        elif temp == '06':
            seat.stat68 = False
        elif temp == '08':
            seat.stat810 = False
        elif temp == '10':
            seat.stat1012 = False
        elif temp == '12':
            seat.stat1214 = False
        elif temp == '14':
            seat.stat1416 = False
        elif temp == '16':
            seat.stat1618 = False
        elif temp == '18':
            seat.stat1820 = False
        elif temp == '20':
            seat.stat2022 = False
        elif temp == '22':
            seat.stat2224 = False
    seat.save()
    # 提交订单
    o = Order()
    o.user = UserProfile.objects.get(user=request.user)
    o.source = seat
    o.price = request.POST.get('sum_price')
    o.order_time = string
    o.save()
    return redirect('order')


# --------------------- 订单 ---------------------------------------------------------------
@login_required
def order(request):
    u = UserProfile.objects.get(user=request.user)
    finish = Order.objects.filter(Q(status='1') & Q(user=u))
    now = Order.objects.filter(Q(status='0') & Q(user=u))
    cancel = Order.objects.filter(Q(status='2') & Q(user=u))
    # print(finish, now, cancel)
    t = ''
    if now:
        t= now[0]
    return render(request, 'My_Orders.html', {
        'finish': finish, 'now': t, 'cancel': cancel
    })


@login_required
def cancel_order(request):
    u = UserProfile.objects.get(user=request.user)
    n = Order.objects.filter(Q(status='0') & Q(user=u))
    myclock = n[0].order_time[:2]
    nowclock = time.strftime("%H", time.localtime())
    print(nowclock, int(nowclock), myclock, nowclock < myclock)
    if int(nowclock) < int(myclock):
        tt = Order.objects.get(id=n[0].id)
        tt.status = '2'
        print(tt.status)
        tt.save()
        print(tt.status)
        seat = UserPrakSeat.objects.get(id=tt.source.id)
# 车位的时间使用状态对应订单里的order_time改变为True；
        times = tt.order_time.split(',')
# print(times[:-1])
        for temp in times[:-1]:
            temp = temp[:2]
            if temp == '00':
                seat.stat02 = True
            elif temp == '02':
                seat.stat24 = True
            elif temp == '04':
                seat.stat46 = True
            elif temp == '06':
                seat.stat68 = True
            elif temp == '08':
                seat.stat810 = True
            elif temp == '10':
                seat.stat1012 = True
            elif temp == '12':
                seat.stat1214 = True
            elif temp == '14':
                seat.stat1416 = True
            elif temp == '16':
                seat.stat1618 = True
            elif temp == '18':
                seat.stat1820 = True
            elif temp == '20':
                seat.stat2022 = True
            elif temp == '22':
                seat.stat2224 = True
        seat.save()
    return redirect('order')


@login_required
def self_lock(request, parkId):
    t = Lock_Seat.objects.get(seat=UserPrakSeat.objects.get(id=parkId))
    return render(request, 'Self_Lock.html', {'parkid': parkId, 'status': t.status})


@login_required
def self_lock_lock(request, parkId):
    t = Lock_Seat.objects.get(seat=UserPrakSeat.objects.get(id=parkId))
    t.status = True
    t.save()
    return redirect('self_lock', parkId=parkId)


@login_required
def self_lock_unlock(request, parkId):
    t = Lock_Seat.objects.get(seat=UserPrakSeat.objects.get(id=parkId))
    t.status = False
    t.save()
    return redirect('self_lock', parkId=parkId)


@login_required
def lock(request, parkId, orderId):
    t = Lock_Seat.objects.get(seat=UserPrakSeat.objects.get(id=parkId))
    return render(request, 'Lock.html', {'parkid': parkId, 'status': t.status, 'orderid': orderId})


@login_required
@csrf_exempt
def lock_start(request):  # 开始订单，同时解锁
    try:
        parkId = request.POST.get('pid')
        seat = UserPrakSeat.objects.get(id=parkId)
        t = Lock_Seat.objects.get(seat=seat)
        t.status = False
        t.save()
        o = Order.objects.get(id=request.POST.get('oid'))
        o.start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        o.save()
        return HttpResponse("ok")
    except Exception as e:
        print(e)
        return HttpResponse("error")


@csrf_exempt
def lock_stop(request):  # 结束订单，同时上锁;改变订单的结束时间、价钱、状态显示完成1;车锁对应表改变状态为True锁定；
    try:  # 车位的时间使用状态对应订单里的order_time改变为True；钱包余额扣款；钱包明细增加。
        parkId = request.POST.get('pid')
        # 改变订单的结束时间、价钱、状态显示完成1;
        o = Order.objects.get(id=request.POST.get('oid'))
        seat = UserPrakSeat.objects.get(id=parkId)
        nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        nowTime = datetime.datetime.strptime(nowTime, '%Y-%m-%d %H:%M:%S')
        x = int(o.order_time[:2])
        o.end_time = nowTime
        print(o.start_time, nowTime, x)
        cha_time = nowTime - o.start_time
        print(cha_time.days,  cha_time.seconds)
        price = 0.00
        msg =''
        n = 1
        if cha_time.days > 0:
            price = seat.price * 24
            msg = '：由于您时间超时，按24小时停车扣款'
        else:
            sum = int(cha_time.seconds) + 3600
            n = int(sum / 3600)
            print('*-', int(sum / 3600))
            price = seat.price * n
        o.price = price
        o.status = '1'
        print('n=', n, price, '-------')
        # 车位的时间使用状态对应订单里的order_time改变为True；
        times = o.order_time.split(',')
        # print(times[:-1])
        for temp in times[:-1]:
            temp = temp[:2]
            if temp == '00':
                seat.stat02 = True
            elif temp == '02':
                seat.stat24 = True
            elif temp == '04':
                seat.stat46 = True
            elif temp == '06':
                seat.stat68 = True
            elif temp == '08':
                seat.stat810 = True
            elif temp == '10':
                seat.stat1012 = True
            elif temp == '12':
                seat.stat1214 = True
            elif temp == '14':
                seat.stat1416 = True
            elif temp == '16':
                seat.stat1618 = True
            elif temp == '18':
                seat.stat1820 = True
            elif temp == '20':
                seat.stat2022 = True
            elif temp == '22':
                seat.stat2224 = True
        # 车锁对应表改变状态为True锁定；
        t = Lock_Seat.objects.get(seat=seat)
        t.status = True
        # 钱包余额扣款；钱包明细增加。
        # 付款的人
        u = UserProfile.objects.get(user=request.user)
        u.account = u.account - price
        u.save()
        uw = WalletDetail()
        uw.user = u
        uw.source = '车位编号：P' + str(seat.id)
        uw.price = price
        uw.note = '停车扣款' + msg
        # 收款的人
        seat.user.account = seat.user.account + Decimal(float(price)*0.8)
        sw = WalletDetail()
        sw.user = seat.user
        sw.source = '车位收入：P' + str(seat.id)
        sw.price = Decimal.from_float(float(price) * 0.8)
        sw.status = False
        sw.note = '车位收入：扣除20%的手续费'
        # 存数据
        o.save()
        seat.save()
        t.save()
        u.save()
        uw.save()
        seat.user.save()
        sw.save()
        return HttpResponse("ok")
    except Exception as e:
        print(e)
        return HttpResponse("error")


# ----------------qita-------------------------------------------------------------------------
def test(request):
    return render(request, 'base.html')


