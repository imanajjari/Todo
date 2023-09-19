from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from django.views import View
from django.shortcuts import redirect



# Create your views here.

# class IndexView(LoginRequiredMixin,ListView):
#     model = Post
#     template_name = 'todo/index.html'
    
#     def get_queryset(self):
#         post = Post.objects.all().order_by('-status')
#         return super().get_queryset()

class IndexView(TemplateView):
    """
    a class based view to show index page
    """

    template_name = "todo/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "ali"
        # context["posts"] = Post.objects.all()
        return context

class ItemDetailView(LoginRequiredMixin,DetailView):
    model = Post
    template_name = 'todo/post_detail.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    '''
    create new task , just complit title 
    '''
    model = Post
    fields = ["title"]
    success_url = '/todo/items/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostCreateView(LoginRequiredMixin,CreateView):
    '''
    create new task 
    '''
    model = Post
    fields = ['title', 'content', 'category', 'published_date']
    template_name = 'todo/post_form.html'
    success_url = '/todo/items/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostEditView(LoginRequiredMixin,UpdateView):
    model = Post
    fields = ['title', 'content', 'category', 'published_date']
    template_name = 'todo/post_form.html'
    success_url = '/todo/items/'


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = '/todo/items/'

class TaskComplete(LoginRequiredMixin, View):
    '''
    chenge status to True => task is done
    '''
    model = Post
    success_url =  '/todo/items/'

    def get(self, request, *args, **kwargs):
        object = Post.objects.get(id=kwargs.get("pk"))
        object.status = True
        object.save()
        return redirect(self.success_url)

class TaskStart(LoginRequiredMixin, View):
    '''
    chenge status to False
    '''
    model = Post
    success_url =  '/todo/items/'

    def get(self, request, *args, **kwargs):
        object = Post.objects.get(id=kwargs.get("pk"))
        object.status = False
        object.save()
        return redirect(self.success_url)

class IndexApiView(TemplateView):
    template_name = 'todo/post_list_api.html'

