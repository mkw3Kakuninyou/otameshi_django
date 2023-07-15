from django.urls import path, include
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.PostIndex, name='index'),
    path('post_create', views.PostCreate.as_view(), name='post_create'),
    path('post_detail/<int:pk>', views.PostDetail, name='post_detail'),
    path('post_update/<int:pk>', views.PostUpdate.as_view(), name='post_update'),
    path('post_delete/<int:pk>', views.PostDelete.as_view(), name='post_delete'),
    path('post_list', views.PostList, name='post_list'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('signup', views.SingUp.as_view(), name='signup'),
    path('like/<int:pk>', views.Like_add, name='like_add'),
    path('like_list', views.LikeList.as_view(), name='like_list'),
    path('like_list_delete/<int:pk>', views.LikeListDelete.as_view(), name='like_list_delete'),
    path('category_list', views.CategoryList.as_view(), name='category_list'),
    path('category_detail/<str:name_en>', views.CategoryDetail.as_view(), name='category_detail'),
    path('category_create', views.CategoryCreate.as_view(), name='category_create'),
    path('search', views.Search, name='search'),
    path('bbs_create', views.BBSCreate.as_view(), name='bbs_create'),
    path('bbs_list', views.BBSList, name='bbs_list'),
    path('bbs_update/<int:pk>', views.BBSUpdate.as_view(), name='bbs_update'),
    path('bbs_delete/<int:pk>', views.BBSDelete.as_view(), name='bbs_delete'),
    path('seo_create', views.SEOCreate.as_view(), name='seo_create'),
    path('seo_list', views.SEOList, name='seo_list'),
    path('seo_update/<int:pk>', views.SEOUpdate.as_view(), name='seo_update'),
    path('layout_create', views.LayoutCreate.as_view(), name='layout_create'),
    path('layout_list', views.LayoutList, name='layout_list'),
    path('layout_update/<int:pk>', views.LayoutUpdate.as_view(), name='layout_update'),
]