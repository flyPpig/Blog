# coding: utf-8

import markdown
from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.utils.six import python_2_unicode_compatible


@python_2_unicode_compatible
class Category(models.Model):

    """
    文章分类模型
    name : 分类名
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


@python_2_unicode_compatible
class Tag(models.Model):

    """
    文章标签
    name : 标签名
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


@python_2_unicode_compatible
class Post(models.Model):

    """
    文章模型
    author          : 作者
    body            : 正文
    category        : 分类
    excerpt         : 摘要
    created_time    : 创建时间
    modified_time   : 修改时间
    tags            : 标签
    title           : 标题
    """

    author = models.ForeignKey(User)
    body = models.TextField()
    category = models.ForeignKey(Category)
    excerpt = models.CharField(max_length=200, blank=True)

    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now_add=True)

    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=70)

    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    # 获取文章的url
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    # 阅读量+1
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):

        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite', ])

            self.excerpt = strip_tags(md.convert(self.body))[:54]

        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_time', 'title']
