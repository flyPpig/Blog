# coding: UTF-8

from django.shortcuts import render, redirect
from .forms import RegisterForm


def register(request):

    # 只有请求为POST时，才表示用户提交了注册信息
    if request.method == 'POST':
        # request.POST 记录了用户提交的注册信息
        # 实例化一个用户表单
        form = RegisterForm(request.POST)

        # 验证合法性
        if form.is_valid():
            # 保存至数据库
            form.save()
            # 注册成功，跳转回首页
            return redirect('/')

    else:
        form = RegisterForm()

    return render(request, 'users/register.html', context={'form': form})
