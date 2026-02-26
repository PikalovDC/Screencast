from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое', blank=True, null=True)
    preview = models.ImageField(upload_to='blogs/', verbose_name='Превью', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров',editable=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'запись блога'
        verbose_name_plural = 'записи блога'
        ordering = ['-created_at']