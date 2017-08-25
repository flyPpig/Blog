
from django.db import models
from django.utils.six import python_2_unicode_compatible


@python_2_unicode_compatible
class Comment(models.Model):

    """
    评论
    name         : 姓名
    email        : 邮箱
    url          : 个人网站
    text         : 评论内容
    created_time : 评论时间
    post         : 评论的文章
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    url = models.URLField(blank=True)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey('blog.Post')

    def __str__(self):
        return self.text[:20]

    class Meta:
        ordering = ['-created_time', 'name']
