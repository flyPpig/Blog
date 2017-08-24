# coding: UTF-8

from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post

from .models import Comment
from .forms import CommentForm


def post_comment(request, post_pk):
    """
    提交评论
    """
    # 先获取被评论的文章
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        # 生成表单
        form = CommentForm(request.POST)

        # 检查数据合法性
        if form.is_valid():
            comment = form.save(commit=False)
            # 关联评论与文章
            comment.post = post
            comment.save()
            return redirect(post)

        else:
            comment_list = post.comment_set.all()
            context = {'post': post, 'form': form,
                       'comment_list': comment_list}
            return render(request, 'blog/detail.html', context=context)

    # 不是post请求，重定向到文章详情
    return redirect(post)
