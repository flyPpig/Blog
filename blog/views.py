# coding: utf-8

import markdown
from .models import *
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from comments.forms import CommentForm

from django.utils.text import slugify
from markdown.extensions.toc import TocExtension


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
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # 获取传给模板的数据,context是一个字典
        context = super().get_context_data(**kwargs)
        # paginator 是 Paginator 的一个实例
        # page_obj 是 Page 的一个实例
        # is_paginated 是一个布尔变量，指示是否分页
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)

        return context

    def pagination_data(self, paginator, page, is_paginated):
        # 不需要分页
        if not is_paginated:
            return {}

        left = []
        right = []
        left_has_more = False
        right_has_more = False
        # 指示是否显示第一页
        first = False
        # 指示是否显示最后一页
        last = False

        # 当前页码
        page_number = page.number
        # 分页后的总页数
        total_pages = paginator.num_pages
        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        if page_number == 1:
            # 若当前为第一页，左边不需要页码数据，只需获取右边的后两页
            right = page_range[page_number:page_number + 2]

            # 若最右边的页码值比最后一页页码值减去 1 还要小
            # 说明最右边的页码与最后一页之间还要其他页码
            # 将 right_has_more置 为 True
            if right[-1] < total_pages - 1:
                right_has_more = True
            # 若最右边的页码值比最后一页页码值小
            # 需要显示最后一页，将 last 置为 True
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 若当前为最后一页，那么右边不需要页码，只需获取左边的前两页
            left = page_range[
                (page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 若最左边的页码值比 2 大
            # 说明与第一页之间还要其他页
            # 将 left_has_more 置为True
            if left[0] > 2:
                left_has_more = True
            # 若最左边的页码值比第一页页码值大
            # 需要显示第一页，将 first 置为 True
            if left[0] > 1:
                first = True

        else:
            # 若当前页既不是最后一页也不是第一页
            # 左边显示前两页，右边显示后两页
            left = page_range[
                (page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否显示最后一页及前面的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否显示第一页及后面的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'first': first,
            'last': last,
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
        }
        return data

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
        # post.body = markdown.markdown(post.body,
        #                               extensions=[
        #                                   'markdown.extensions.extra',
        #                                   'markdown.extensions.codehilite',
        #                                   'markdown.extensions.toc',
        #                               ])
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 'markdown.extensions.toc',
            TocExtension(slugify=slugify)
        ])
        post.body = md.convert(post.body)
        post.toc = md.toc
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


class TagView(ListView):

    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):

        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)
