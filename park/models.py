from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone as timezone


# 用户数据表
class UserProfile(models.Model):
    # 建立与User模型之间的关系. 账户名即为手机号
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # 想增加的属性
    account = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    gender = models.BooleanField(default=True)  # 性别：默认男
    qq = models.CharField(max_length=12)
    weixin = models.CharField(max_length=20)
    licence_number = models.CharField(max_length=20)  # 车牌号
    has_seat = models.BooleanField(default=False)  # 是否有注册车位
    seat_number = models.CharField(max_length=40)  # 车位号
    id_number = models.CharField(max_length=18)  # 身份证

    def __str__(self):
        return self.user.username


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


# 支付订单表
# class Order(models.Model):
#     source = models.CharField(max_length=500, blank=False)
#     time = models.DateTimeField(default=timezone.now)
#     price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)  # 单价
