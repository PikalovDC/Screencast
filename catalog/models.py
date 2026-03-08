from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name']


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория', related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за покупку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Владелец', related_name='products')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ['title']
        permissions = [
            ("can_unpublish_product", "can unpublished product")
        ]
