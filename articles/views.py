from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

# Create your views here.

class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'

class ArticleUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Article
    fields = ('title', 'summary', 'body', 'photo',)
    template_name = 'article_edit.html'
# test qiladi chunki userdan boshqalar kirib uni
# o'zgartirmasligi uchun
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class ArticleDeleteView(LoginRequiredMixin,  UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

# LoginRequiredMixin bu agar login qilmagan bo'lsangiz login qiling deb
# login oynasini ochib berish uchun mixin
class ArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = ('title', 'summary', 'body', 'photo',)

    # postlarni boshqa userlar o'chirmasligi yoki usernameni o'zgartirmasligi 
    # uchun funksiya
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


    # user superuser ekanini tekshirish
    def test_func(self):
        return self.request.user.is_superuser

