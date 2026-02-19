from django.shortcuts import render
from django.http import HttpResponse
from blog.models import BlogPost
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.urls import reverse_lazy

class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save(update_fields=['views_count'])
        return obj

class BlogCreateView(CreateView):
    model = BlogPost
    fields =['title', 'content', 'preview', 'is_published']
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        messages.success(self.request, 'Запись успешно создана')
        return super().form_valid(form)

class BlogUpdateView(UpdateView):
    model = BlogPost
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blog/blog_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Запись успешно обновлена')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:detail', kwargs={'pk': self.object.pk})

class BlogDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:list')
    context_object_name = 'post'

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Запись успешно удалена')
        return super().delete(request, *args, **kwargs)

