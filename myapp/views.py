from django.shortcuts import render, resolve_url, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from .models import Post, Like, Category, BBS, SEO, Layout
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import PostForm, LoginForm, SingUpForm, SearchForm, BBSForm, CategoryForm, SEOForm, LayoutForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
import os


#参考)https://djangobrothers.com/blogs/django_pagination/
def PostIndex(request):
    if request.POST.get('order')=='投稿日-新しい順':
        post_list = Post.objects.all().order_by('-created_at')
    elif request.POST.get('order')=='投稿日-古い順':
        post_list = Post.objects.all().order_by('created_at')
    elif request.POST.get('order')=='更新日-新しい順':
        post_list = Post.objects.all().order_by('-updated_at')
    elif request.POST.get('order')=='更新日-古い順':
        post_list = Post.objects.all().order_by('updated_at')
    elif request.POST.get('order')=='カテゴリごと':
        post_list = Post.objects.all().order_by('category')
    elif request.POST.get('order')=='投稿者ごと':
        post_list = Post.objects.all().order_by('author')
    else:
        post_list = Post.objects.all().order_by('-created_at')
    
    paginator = Paginator(post_list, 6)
    p = request.GET.get('page')
    post_list = paginator.get_page(p)
    return render(request, 'myapp/index.html', {'page_obj': post_list}) #Keyの「page_obj」はpagination.html(どこかのサイトからお借りしたもの)に対応するようにしている．
    
    
class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('myapp:index')
    template_name = os.path.join('myapp', 'post_create.html')
    
    def form_valid(self, form):
        form.instance.author_id = self.request.user.id #Postテーブルのauthorカラム(Userテーブル((from django.contrib.auth.models import User)を参照している)に対して，現在ログインしているユーザーのidを設定する．
        return super().form_valid(form)

    
    def get_success_url(self): #base.htmlの{{ if messages }}以下の箇所に対応
        messages.success(self.request, '投稿を登録しました。')
        return resolve_url('myapp:index')    
    

def PostDetail(request, pk):
    detail_data = Post.objects.get(pk = pk)
    category_posts = Post.objects.filter(category = detail_data.category).order_by('-created_at')[:5] #現在参照している記事と同じカテゴリの記事を表示させる
    like_delete = Like.objects.filter(post_id = pk).first() #お気に入り削除用（「Postテーブルのid = Likeテーブルのpost_id」となるデータの主キーを取得する）    

    views_count = get_object_or_404(Post, id = pk) #記事が参照された回数を数える
    views_count.views += 1
    views_count.save() 

    if request.user.is_active: #ユーザーがログインしている場合は，Likeテーブルのuserカラムのデータで，現在ログインしているユーザーのid(詳細はUserテーブル(from django.contrib.auth.models import User))と一致するものを以下のis_likeで取得する．
        is_like = Like.objects.values_list('post', flat=True).filter(user=request.user) #values_listは特定のカラム(ここではpost)の値をリストで取得する．
        logged_in_params = {
            'is_like': is_like,
            'like_delete': like_delete,
            'object': detail_data,
            'category_posts': category_posts,
            'pk': pk,
            'views_count': views_count,
        }
        return render(request, 'myapp/post_detail.html', logged_in_params)
    else:
        not_logged_in_params = {
            'object': detail_data,
            'category_posts': category_posts,
            'pk': pk,
            'views_count': views_count,
        }
        return render(request, 'myapp/post_detail.html', not_logged_in_params)


class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'myapp/post_update.html'
    
    def get_success_url(self): #base.htmlの{{ if messages }}以下の箇所に対応
        messages.info(self.request, '投稿を更新しました。')
        return resolve_url('myapp:post_detail', pk=self.kwargs['pk'])
    
    
class PostDelete(DeleteView):
    model = Post
    template_name = 'myapp/post_delete.html'
    
    def get_success_url(self): #base.htmlの{{ if messages }}以下の箇所に対応
        messages.info(self.request, '投稿を削除しました。')
        return resolve_url('myapp:index')
    
    
#参考)https://djangobrothers.com/blogs/django_pagination/
def PostList(request):
    if request.POST.get('order')=='投稿日-新しい順':
        post_list = Post.objects.all().order_by('-created_at')
    elif request.POST.get('order')=='投稿日-古い順':
        post_list = Post.objects.all().order_by('created_at')
    elif request.POST.get('order')=='更新日-新しい順':
        post_list = Post.objects.all().order_by('-updated_at')
    elif request.POST.get('order')=='更新日-古い順':
        post_list = Post.objects.all().order_by('updated_at')
    elif request.POST.get('order')=='カテゴリごと':
        post_list = Post.objects.all().order_by('category')
    elif request.POST.get('order')=='投稿者ごと':
        post_list = Post.objects.all().order_by('author')
    else:
        post_list = Post.objects.all().order_by('-created_at')
    
    paginator = Paginator(post_list, 20)
    p = request.GET.get('page')
    post_list = paginator.get_page(p)
    return render(request, 'myapp/post_list.html', {'page_obj': post_list}) #Keyの「page_obj」はpagination.html(どこかのサイトからお借りしたもの)に対応するようにしている．


"""
ログインについては，settings.pyでも以下のように設定しなければならない．
LOGIN_URL = 'myapp:login'
LOGIN_REDIRECT_URL = 'myapp:index' 
"""
class Login(LoginView):
    form_class = LoginForm
    template_name = 'myapp/login.html'
    
    
class Logout(LogoutView):
    template_name = 'myapp/logout.html'
    

class SingUp(CreateView):
    form_class = SingUpForm
    template_name = 'myapp/signup.html'
    success_url = reverse_lazy('myapp:index')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user) #login関数は「from django.contrib.auth import login」を記載して利用する & ユーザー登録と同時にログインする．
        self.object = user
        messages.info(self.request, 'ユーザー登録をしました。') #base.htmlの{{ if messages }}以下の箇所に対応
        return HttpResponseRedirect(self.get_success_url())


@login_required
def Like_add(request, pk):
    post = Post.objects.get(pk = pk)
    is_like = Like.objects.values_list('post', flat=True).filter(user=request.user) #ユーザーがログインしている場合は，Likeテーブルのuserカラムのデータで，現在ログインしているユーザーのid(詳細はUserテーブル(from django.contrib.auth.models import User))と一致するものをis_likeで取得する．values_listは特定のカラム(ここではpost)の値をリストで取得する．
    if pk not in is_like: #現在参照している記事のid(Postテーブルのid)がLikeテーブルのpostカラムに存在しない場合に，「お気に入り登録する」ボタンを押すと，現在参照している記事のid，現在ログインしているユーザーのid(詳細はUserテーブル(from django.contrib.auth.models import User))がLikeテーブルに登録される．
        like = Like()
        like.user = request.user
        like.post = post
        like.save()
        messages.success(request, 'お気に入りに登録しました！') #base.htmlの{{ if messages }}以下の箇所に対応
        return redirect('myapp:post_detail', pk)


class LikeList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'myapp/like_list.html'
    paginate_by = 20
    
    def get_queryset(self):
        return Like.objects.filter(user=self.request.user).order_by('-post') #Likeテーブルのuserカラムのデータで，現在ログインしているユーザーのid(詳細はUserテーブル(from django.contrib.auth.models import User))と一致するものを取得する．


class LikeListDelete(LoginRequiredMixin, DeleteView):
    template_name = 'myapp/like_list_delete.html'
    model = Like
    
    def get_success_url(self):
        messages.info(self.request, 'お気に入りから削除しました。') #base.htmlの{{ if messages }}以下の箇所に対応
        return resolve_url('myapp:like_list')


class CategoryList(ListView):
    model = Category
    template_name = os.path.join('myapp', 'category_list.html')
    paginate_by = 9
    
    
class CategoryDetail(DetailView):
    model = Category
    slug_field = 'name'
    slug_url_kwarg = 'name'
    
    def get_context_data(self, *args, **kwargs):
        detail_data = Category.objects.get(name = self.kwargs['name']) #objects.getはデータを1つだけ取得する．self.kwargs['name_en']はurls.pyのpath('category_detail/<str:name_en>(省略))である．
        category_posts = Post.objects.filter(category = detail_data.id).order_by('-created_at')
        
        context = {
            'object': detail_data,
            'category_posts': category_posts,
        }
        
        return context


class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'myapp/Category_create.html'
    success_url = reverse_lazy('myapp:index')
    

    def get_success_url(self):
        messages.success(self.request, '新たにカテゴリを登録しました。') #base.htmlの{{ if messages }}以下の箇所に対応
        return resolve_url('myapp:index')  


def Search(request):
    if request.method == 'POST':
        searchform = SearchForm(request.POST) #実行結果<QueryDict: {'csrfmiddlewaretoken': ['省略'], 'freeword': ['検索欄に入力された値']}>
        if searchform.is_valid():
            freeword = searchform.cleaned_data['freeword'] #検索欄に入力された値を文字列化(消毒(サニタイズ))する．「freeword」はinputタグのnameの値である．
            search_list = Post.objects.filter(Q(title__icontains = freeword)|Q(content__icontains = freeword)|Q(description__icontains = freeword)).order_by('-created_at') #「カラム名__icontains = freename」は「そのカラムのデータでfreewordを含むもの」ということ．
            
            #参考)https://djangobrothers.com/blogs/django_pagination/
            if request.POST.get('order')=='投稿日-新しい順':
                post_list = search_list.order_by('-created_at')
            elif request.POST.get('order')=='投稿日-古い順':
                post_list = search_list.all().order_by('created_at')
            elif request.POST.get('order')=='更新日-新しい順':
                post_list = search_list.all().order_by('-updated_at')
            elif request.POST.get('order')=='更新日-古い順':
                post_list = search_list.all().order_by('updated_at')
            elif request.POST.get('order')=='カテゴリごと':
                post_list = search_list.all().order_by('category')
            elif request.POST.get('order')=='投稿者ごと':
                post_list = search_list.all().order_by('author')
            else:
                post_list = search_list.all().order_by('-created_at')
            
            paginator = Paginator(post_list, 6)
            p = request.GET.get('page')
            post_list = paginator.get_page(p)
            search_context={
                'page_obj': post_list,
                'freeword': freeword,
            }
            return render(request, 'myapp/search.html', search_context) #Keyの「page_obj」はpagination.html(どこかのサイトからお借りしたもの)に対応するようにしている．

    else:
        return redirect('myapp:index')


class BBSCreate(LoginRequiredMixin, CreateView):
    model = BBS
    form_class = BBSForm
    template_name = 'myapp/bbs_create.html'
    success_url = reverse_lazy('myapp:index')

    def get_success_url(self):
        messages.info(self.request, '掲示板を作成しました。') #base.htmlの{{ if messages }}以下の箇所に対応
        return resolve_url('myapp:index')


def BBSList(request):
    bbs_list = BBS.objects.all().order_by('-bbscontent')
    context = {
        'bbs_list': bbs_list,
    }
    return render(request, 'myapp/bbs_list.html', context)


class BBSUpdate(UpdateView):
    model = BBS
    form_class = BBSForm
    template_name = 'myapp/bbs_update.html'
    
    def get_success_url(self):
        messages.info(self.request, '掲示板を更新しました。') #base.htmlの{{ if messages }}以下の箇所に対応
        return resolve_url('myapp:index')


class BBSDelete(LoginRequiredMixin, DeleteView):
    template_name = 'myapp/bbs_delete.html'
    model = BBS
    
    def get_success_url(self):
        messages.info(self.request, '掲示を削除しました．') #base.htmlの{{ if messages }}以下の箇所に対応
        return resolve_url('myapp:bbs_list')


class SEOCreate(LoginRequiredMixin, CreateView):
    model = SEO
    form_class = SEOForm
    template_name = 'myapp/seo_create.html'
    success_url = reverse_lazy('myapp:index')

    def get_success_url(self):
        messages.info(self.request, 'SEOを作成しました。') #base.htmlの{{ if messages }}以下の箇所に対応
        return resolve_url('myapp:index')


@login_required
def SEOList(request): #base.htmlにmodels.pyのSEOテーブルのデータを渡すためにcontext_processors.pyにも同じような関数を定義している．
    pass

    return render(request, 'myapp/seo_list.html')


class SEOUpdate(LoginRequiredMixin, UpdateView):
    model = SEO
    form_class = SEOForm
    template_name = 'myapp/seo_update.html'
    
    def get_success_url(self):
        messages.info(self.request, 'SEOを更新しました。') #base.htmlの{{ if messages }}以下の箇所に対応
        return resolve_url('myapp:index')


class LayoutCreate(LoginRequiredMixin, CreateView):
    model = Layout
    form_class = LayoutForm
    template_name = 'myapp/layout_create.html'
    success_url = reverse_lazy('myapp:index')

    def get_success_url(self):
        messages.info(self.request, 'ページレイアウトを作成しました。') #base.htmlの{{ if messages }}以下の箇所に対応
        return resolve_url('myapp:index')


def LayoutList(request): #base.htmlにmodels.pyのLayoutテーブルのデータを渡すためにcontext_processors.pyにも同じような関数を定義している．
    pass

    return render(request, 'myapp/layout_list.html')


class LayoutUpdate(LoginRequiredMixin, UpdateView):
    model = Layout
    form_class = LayoutForm
    template_name = 'myapp/layout_update.html'
    
    def get_success_url(self):
        messages.info(self.request, 'ページレイアウトを更新しました。') #base.htmlの{{ if messages }}以下の箇所に対応
        return resolve_url('myapp:index')