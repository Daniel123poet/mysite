import datetime
from django.shortcuts import render_to_response, render, redirect
from django.contrib.contenttypes.models import ContentType 
from django.db.models import Sum
from django.utils import timezone
from django.core.cache import cache
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data,get_yesterday_hot_data
from blog.models import Blog
# from .forms import LoginForm, RegForm


def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    #筛选小于今天,大于等于7天前的
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=date) \
                        .values('id', 'title') \
                        .annotate(read_num_sum=Sum('read_details__read_num')) \
                        .order_by('-read_num_sum')
    return blogs[:7]


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)
    today_hot_data = get_today_hot_data(blog_content_type)
    yesterday_hot_data =  get_yesterday_hot_data(blog_content_type)
    hot_blogs_for_7_days = get_7_days_hot_blogs()

    #获取7天热门博客的缓存数据
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_7_days_hot_blogs()
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 3600) #缓存里没有就先放到缓存里然后设置有效期
        print('calculate')
    else:
        print('use cache')  #有就使用缓存

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = today_hot_data
    context['yesterday_hot_data'] = yesterday_hot_data
    context['hot_blogs_for_7_days'] = hot_blogs_for_7_days
    return render(request,'home.html', context)



