from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField('カテゴリ名', max_length=50)
    name_en = models.CharField('カテゴリ名英語', max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def post_count(self):
        n = Post.objects.filter(category = self).count() #Postテーブルのcategoryカラムに，そのカテゴリーが登録されている件数を取得する(category_list.htmlで使用)
        return n
    
    def __str__(self):
        return self.name  


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT, blank=False)
    title = models.CharField('タイトル', max_length=50)
    description = models.TextField('概要', max_length=100)
    content = models.TextField('内容', max_length=10000, blank=True, null=False)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    thumbnail = models.ImageField(upload_to='images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    
    def like_count(self):
        n = Like.objects.filter(post = self).count() #Likeテーブルのpostカラムに，その記事が登録されている件数を取得する(index.htmlで使用)．
        return n
        
    def __str__(self):
        return self.title
    
    
class Like(models.Model):
    post = models.ForeignKey(Post, verbose_name="投稿", on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name="Likeしたユーザー", on_delete=models.PROTECT)

    def __str__(self):
        return self.post


class BBS(models.Model):
    bbscontent = models.TextField('掲示板', max_length=100)

    def __str__(self):
        return self.bbscontent


class SEO(models.Model): 
    meta_keywords = models.CharField(verbose_name='metaタグ(name="keywords")', max_length=30)
    meta_description = models.CharField(verbose_name='metaタグ(name="description")', max_length=120)
    meta_prop_ogTitle = models.CharField(verbose_name='metaタグ(property="og:title")', max_length=30)
    meta_prop_ogImage = models.ImageField(verbose_name='metaタグ(property="og:image")', upload_to='images/', blank=True)
    meta_prop_ogWidth = models.PositiveSmallIntegerField(verbose_name='metaタグ(property="og:image:width")', blank=True)
    meta_prop_ogHeight = models.PositiveSmallIntegerField(verbose_name='metaタグ(property="og:image:height")', blank=True)
    meta_prop_ogDescription = models.CharField(verbose_name='metaタグ(property="og:description")', max_length=120, blank=True)
    meta_prop_ogSiteName = models.CharField(verbose_name='metaタグ(property="og:site_name")', max_length=30, blank=True)
    meta_prop_ogUrl = models.URLField(verbose_name='metaタグ(property="og:url")', blank=True)
    meta_twi_imgSrc = models.ImageField(verbose_name='metaタグ(name="twitter:image:src")', upload_to='images/', blank=True)
    meta_twi_title = models.CharField(verbose_name='metaタグ(name="twitter:title")', max_length=120, blank=True)
    page_title = models.CharField(verbose_name='ページタイトル', max_length=25, blank=True)
    

class Layout(models.Model):
    home_top_title = models.CharField(verbose_name='トップタイトル', max_length=25)
    home_sub_title = models.CharField(verbose_name='サブタイトル', max_length=25, blank=True)
    