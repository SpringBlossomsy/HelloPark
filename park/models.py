from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone as timezone


# 用户数据表
class UserProfile(models.Model):
    # 建立与User模型之间的关系. 账户名即为手机号
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # 想增加的属性
    account = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    # gender = models.BooleanField(default=True)  # 性别：默认男
    # qq = models.CharField(max_length=12)
    # weixin = models.CharField(max_length=20)
    licence_number = models.CharField(max_length=20)  # 车牌号
    # has_seat = models.BooleanField(default=False)  # 是否有注册车位
    # seat_number = models.CharField(max_length=40)  # 车位号
    # id_number = models.CharField(max_length=18)  # 身份证

    def __str__(self):
        return self.user.username

# 用户停车位
class UserPrakSeat(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    lat = models.DecimalField(max_digits=12, decimal_places=6, blank=False)  # 坐标
    lng = models.DecimalField(max_digits=12, decimal_places=6, blank=False)  # 坐标
    pioaddress = models.CharField(max_length=512, blank=True)  # 位置描述
    note = models.CharField(max_length=2048, blank=True)  # 详细描述
    # 每两个小时单价
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    # 开放时间选择
    time02 = models.BooleanField(default=False)  # 开放时间选择：0:00-02:00
    time24 = models.BooleanField(default=False)
    time46 = models.BooleanField(default=False)
    time68 = models.BooleanField(default=False)
    time810 = models.BooleanField(default=False)
    time1012 = models.BooleanField(default=False)
    time1214 = models.BooleanField(default=False)
    time1416 = models.BooleanField(default=False)
    time1618 = models.BooleanField(default=False)
    time1820 = models.BooleanField(default=False)
    time2022 = models.BooleanField(default=False)
    time2224 = models.BooleanField(default=False)
    # 使用状态
    stat02 = models.BooleanField(default=False)  # 默认有人使用
    stat24 = models.BooleanField(default=False)
    stat46 = models.BooleanField(default=False)
    stat68 = models.BooleanField(default=False)
    stat810 = models.BooleanField(default=False)
    stat1012 = models.BooleanField(default=False)
    stat1214 = models.BooleanField(default=False)
    stat1416 = models.BooleanField(default=False)
    stat1618 = models.BooleanField(default=False)
    stat1820 = models.BooleanField(default=False)
    stat2022 = models.BooleanField(default=False)
    stat2224 = models.BooleanField(default=False)
    # 审核状态
    status = models.CharField(max_length=32, default='0')  # 默认审核未通过0;审核通过1；审核中2；


# 停车位数据表
# class ParkSeat(models.Model):
#     # id车位编号
#     owner_id = models.ForeignKey("UserProfile", on_delete=models.CASCADE)  # 车位主编号
#     parking_lot = models.CharField(max_length=40)  # 停车场
#     floor = models.IntegerField()  # 停车库
#     seat_number = models.CharField(max_length=40)  # 车位号
#     coodinates = models.DecimalField(max_digits=12, decimal_places=6, blank=False)  # 坐标
#     district = models.CharField(max_length=50)  # 街区
#     status = models.BooleanField(default=True)  # 占空状态，默认占用
#     price = models.DecimalField(max_digits=3, decimal_places=1, blank=False)  # 单价
#     open_time = models.CharField(max_length=400)  # 开放时间
#     detail = models.CharField(max_length=1024)  # 详细说明
#
#
# # 停车场数据表
# class Park(models.Model):
#     # 停车场编号、名称、坐标、开放时间
#     name = models.CharField(max_length=40)
#     coordinate = models.DecimalField(max_digits=12, decimal_places=6, blank=False)
#     open_time = models.CharField(max_length=400)  # 开放时间


# 钱包明细表
class WalletDetail(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    source = models.CharField(max_length=500, blank=False)  # 汇款人/支付对象；格式：“车位编号：P1”，“车位收入：P1”
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    status = models.BooleanField(default=True)  # 默认支出
    time = models.DateTimeField(default=timezone.now)
    note = models.CharField(max_length=1024, blank=True)  # 备注


# 用户订单表
class Order(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    source = models.ForeignKey('UserPrakSeat', on_delete=models.CASCADE, related_name='user_source')  # 车位
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    order_time = models.CharField(max_length=2048, blank=True)
    # 订单计费开始时间
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=32, default='0')  # 默认进行中0;已完成1；已取消2；
    note = models.CharField(max_length=1024, blank=True)  # 备注


# 车位锁
class CarLock(models.Model):
    name = models.CharField(max_length=1024, blank=False)  # 车锁名字
    status = models.BooleanField(default=True)  # 车位锁能否使用
    note = models.CharField(max_length=1024, blank=True)  # 备注


# 车锁对应表
class Lock_Seat(models.Model):
    lock = models.ForeignKey('CarLock', on_delete=models.CASCADE, related_name='carlock')
    seat = models.ForeignKey('UserPrakSeat', on_delete=models.CASCADE)
    status = models.BooleanField(default=False)  # 车位锁状态，默认锁关闭

