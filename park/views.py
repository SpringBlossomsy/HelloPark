from django.shortcuts import render
from registration.backends.simple.views import RegistrationView
import re
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
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


class MyRegistrationView(RegistrationView):  # 用户成功注册后重定向到其他页面
    def get_success_url(self, user):
        return reverse('profile', user.username)


def index(request):
    return HttpResponse("--")