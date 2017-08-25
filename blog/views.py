# coding: utf-8

import markdown
from .models import *
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from comments.forms import CommentForm


# def index(request):
#     """
#     首页视图函数
#     """
#     post_list = Post.objects.all()
#     return render(request,
#                   'blog/index.html',
#                   context={'post_list': post_list})

class IndexView(ListView):

    """
    首页视图
    """
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'


# def archives(request, year, month):
#     """
#     归档视图函数
#     """
#     post_list = Post.objects.filter(created_time__year=year,
#                                     created_time__month=month)
#     return render(request, 'blog/index.html', context={'post_list':
#                   post_list})

class ArchivesView(IndexView):

    """
    归档视图
    """

    def get_queryset(self):

        return super(ArchivesView, self).get_queryset().filter(created_time__year=self.kwargs.get('year'),
                                                               created_time__month=self.kwargs.get('month'))

# def category(request, pk):
#     """
#     分类视图函数
#     """
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate)
#     return render(request, 'blog/index.html',
#                   context={'post_list':post_list})


class CategoryView(IndexView):
    """
    分类视图
    """

    def get_queryset(self):

        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


# def detail(request, pk):
#     """
#     文章详情视图函数
#     """
#     post = get_object_or_404(Post, pk=pk)
#     # 阅读量+1
#     post.increase_views()
#     post.body = markdown.markdown(post.body,
#                                   extensions=[
#                                       'markdown.extensions.extra',
#                                       'markdown.extensions.codehilite',
#                                       'markdown.extensions.toc',
#                                   ])
#     form = CommentForm()
#     context = {'post': post, 'form': form}

#     return render(request, 'blog/detail.html', context=context)

class PostDetailView(DetailView):

    """
    文章详情视图
    """
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        """
        覆写 get 方法
        文章被访问一次，阅读量+1
        get 方法返回一个 HttpResponse 实例
        先调用父类 get 方法，获取 Post 模型实例，然后才有 self.object 属性
        """
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        """
        覆写 grt_object 方法的目的是需要对 post 的 body 进行渲染
        """

        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.markdown.toc',
                                      ])
        return post

    def get_context_data(self, **kwargs):
        """
        覆写 get_context_data 方法的目的是将评论表单、评论列表传递给模板
        """
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({'form': form,
                        'comment_list': comment_list})
        return context
