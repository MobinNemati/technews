from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="عنوان")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی ها"


    def __str__(self):
        return self.name

class Post(models.Model):
    image = models.ImageField(upload_to= 'news/', default='news/default.jpg', verbose_name="تصویر")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="نویسنده")
    title = models.CharField(max_length=100, verbose_name="عنوان خبر")
    content = models.TextField(verbose_name="محتوا")
    tags = TaggableManager(verbose_name="تگ ها")
    category = models.ManyToManyField(Category, verbose_name="دسته‌بندی")
    counted_view = models.IntegerField(default=0, verbose_name="تعداد ویو")
    status = models.BooleanField(default=False, verbose_name="وضعیت")
    published_date = models.DateTimeField(null=True, verbose_name="تاریخ انتشار")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")


    class Meta:
        ordering = ['created_date']
        verbose_name = "خبر"
        verbose_name_plural = "خبر ها"

    def __str__(self):
        return ' {} - {} '.format(self.title, self.id)
    
    def get_absolute_url(self):
        return reverse("news:single", kwargs={"pid": self.id})
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="خبر")
    name = models.CharField(max_length=255, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    message = models.TextField(verbose_name="پیام")
    approved = models.BooleanField(default=True, verbose_name="تأییدشده") 
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")


    class Meta:
        ordering = ('-created_date',)
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"

    def __str__(self):
        return self.name