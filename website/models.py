from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    subject = models.CharField(max_length=255, verbose_name="موضوع")
    message = models.TextField(verbose_name="پیام")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        ordering = ('created_date',)

        verbose_name = "تماس"
        verbose_name_plural = "تماس ها"

    def __str__(self):
        return self.name
    

class Newsletter(models.Model):
    email = models.EmailField(verbose_name="ایمیل")

    def __str__(self):
        return self.email


    class Meta:

        verbose_name = "خبرنامه"
        verbose_name_plural = "خبرنامه ها"