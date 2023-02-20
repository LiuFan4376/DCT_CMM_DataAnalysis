from django import http
from django.shortcuts import render
from . import forms, models


# Create your views here.


def login(request):
    if request.method == 'GET':
        myform = forms.UserInfoForm()
        return render(request, 'login.html')
    if request.method == 'POST':
        myform = forms.UserInfoForm({'numbers': request.POST['number'],'password': request.POST['password']})
        if myform.is_valid():
            number = myform.cleaned_data.get('numbers')
            password = myform.cleaned_data.get('password')
            data = models.UserInfo.objects.get(name=number)
            if data.password == password:
                return http.HttpResponse('登录成功')
            else:
                ValueError('密码错误')
                return http.HttpResponse('密码错误')
        else:
            return http.HttpResponse('登录失败')
