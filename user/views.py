import datetime
import string
import random
from django.http import JsonResponse
from django.shortcuts import render_to_response, render, redirect
from django.contrib.contenttypes.models import ContentType 
from django.db.models import Sum
from django.utils import timezone
from django.core.cache import cache
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data,get_yesterday_hot_data
from blog.models import Blog
from .forms import LoginForm, RegForm, ChangeNicknameForm, BindEmailForm
from .models import Profile

def userLogin(request):
    '''username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)
    referer = request.META.get('HTTP_REFERER', reverse('home')) #通过别名解析到首页链接
    if user is not None:
        login(request, user)
        return redirect(referer)
    else:
        return render(request, 'error.html', {'message': '用户名或密码不正确'})'''

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
        
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'user/login.html', context)

def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            #创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            #登录用户
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'user/register.html', context)


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))

def user_info(request):
    context = {}
    return render(request, 'user/user_info.html', context)

def change_nickname(request):

    redirect_to = request.GET.get('from', reverse('home'))

    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST, user = request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)

    else:
        form = ChangeNicknameForm()
        context = {}
        context['form'] = form
        context['page_title'] = '修改昵称'
        context['form_title'] = '修改昵称'
        context['submit_text'] = '修改'
        context['return_back_url'] = redirect_to
        return render(request, 'form.html', context)

def bind_email(request):
    redirect_to = request.GET.get('from', reverse('home'))

    if request.method == 'POST':
        form = BindEmailForm(request.POST, user = request.user)
        if form.is_valid():
            pass
            return redirect(redirect_to)

    else:
        form = BindEmailForm()

        context = {}
        context['form'] = form
        context['page_title'] = '绑定邮箱'
        context['form_title'] = '绑定邮箱'
        context['submit_text'] = '绑定'
        context['return_back_url'] = redirect_to
        return render(request, 'user/bind_email.html', context)

def send_verification_code(request):
    email = request.GET.get('email', '')
    data = {}
    if email != '':
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        request.session['bind_email_code'] = code
        # 发送邮件

        send_mail(
            '绑定邮箱',
            '验证码: %s' % code,
            '616852469@qq.com',
            # 'ding2017yang@163.com',
            [email],
            fail_silently=False,
            )
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'

    return JsonResponse(data)