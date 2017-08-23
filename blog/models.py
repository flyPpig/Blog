# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from django.utils.six import python_2_unicode_compatible


@python_2_unicode_compatible
class Category(models.Model):

    """
    文章分类模型
    slef.name : 分类名
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Tag(models.Model):

    """
    文章标签
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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

    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=70)

    def __str__(self):
        return self.title
