from .models import Category, BBS, SEO, Layout
from django.contrib.auth.models import User
from datetime import date
import datetime


""" settings.pyのTEMPLATES-->'OPTIONS'-->'context_processors'に'myapp.context_processors.関数名'のように記載して主にbase.html(継承元テンプレート)とindex.htmlで利用する． """


def Index(request): #index.htmlで利用する
    bbs = BBS.objects.all()
    registered_users = User.objects.all().count()
    index_context = {
        'bbs': bbs,
        'registered_users': registered_users,
    }
    return index_context


def All_Category(request):
    category_list = Category.objects.all()
    
    params = {
        'category_list': category_list,
    }
    
    return params

def Date(*args, **kwargs):
    today = datetime.date.today()
    current_year = datetime.date.today().year
    Date_context = {
        'today': today,
        'current_year': current_year
    }
    return Date_context


def SEOList(request):
    seo = SEO.objects.first()

    seo_context = {
        'seo': seo,
    }

    return seo_context


def LayoutList(request):
    layout = Layout.objects.first()
    layout_context = {
        'layout': layout,
    }
    return layout_context