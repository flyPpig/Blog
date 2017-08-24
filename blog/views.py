# coding: utf-8

import markdown
from django.shortcuts import render, get_object_or_404
from .models import *
from comments.forms import CommentForm


def index(request):
    """
    首页视图函数
    """
    post_list = Post.objects.all()
    return render(request,
                  'blog/index.html',
                  context={'post_list': post_list})


def archives(request, year, month):
    """
    归档视图函数
    """
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month)
    return render(request, 'blog/index.html', context={'post_list': post_list})


def category(request, pk):
    """
    分类视图函数
    """
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})


def detail(request, pk):
    """
    文章详情视图函数
    """
    post = get_object_or_404(Post, pk=pk)
    # 阅读量+1
    post.increase_views()
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    context = {'post': post, 'form': form}

    return render(request, 'blog/detail.html', context=context)
