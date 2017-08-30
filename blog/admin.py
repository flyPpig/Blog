from django import forms
from django.contrib import admin
from .models import Post, Category, Tag
from ckeditor.widgets import CKEditorWidget


# class PostAdminForm(forms.ModelForm):

#     body = forms.CharField(widget=CKEditorWidget())

#     class Meta:
#         model = Post


class PostAdmin(admin.ModelAdmin):

    #form = PostAdminForm
    list_display = ['title', 'created_time',
                    'modified_time', 'category', 'author']

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
# admin.site.register(PostAdmin)
