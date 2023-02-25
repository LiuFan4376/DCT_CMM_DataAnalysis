import os

from django.http import FileResponse

from DCT_CMM_DataAnalysis import settings
from django import http
from django.shortcuts import render
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate
from . import forms, models
from DataProcessUtil.DataProcess import DataAnalysis, data_processB


# Create your views here.


def login(request):
    if request.method == 'GET':
        myform = forms.UserInfoForm()
        return render(request, 'login.html')
    if request.method == 'POST':
        myform = forms.UserInfoForm({'numbers': request.POST['number'], 'password': request.POST['password']})
        if myform.is_valid():
            number = myform.cleaned_data.get('numbers')
            password = myform.cleaned_data.get('password')
            user = authenticate(username=number, password=password)
            if user:
                return http.HttpResponseRedirect('/data_process/upload')
            else:
                ValueError('密码错误')
                return http.HttpResponse('密码错误')
        else:
            return http.HttpResponse('用户名或密码错误')


def upload_file(request):
    if request.method == 'GET':
        return render(request, 'data_process.html')

    if request.method == 'POST':
        file = request.FILES['myfile']
        select = request.POST['select_program']

        if not file:
            return http.HttpResponse('请选择文件上传')
        if not select:
            return http.HttpResponse('请选择程序')
        # 设置文件储存路径
        save_path = os.path.join(settings.MEDIA_ROOT, file.name)
        with open(save_path, 'wb') as f:
            #  chunks() 而不是 read() 是为了确保即使是大文件又不会将我们系统的内存占满
            for chunk in file.chunks():
                f.write(chunk)
        data_process(save_path, select)
        if select == 'A':
            return render(request, 'result.html')
        else:
            return render(request, 'resultB.html')


def data_process(data_path, program):
    """
    将原始三坐标数据文件进行处理后，模版化输出
    :param program: program: 程序名称
    :param data_path: 待处理数据文件的路径
    :return: None
    """
    data_path = data_path
    module_path = os.path.join(settings.MEDIA_ROOT, '模板.xlsx')
    data_clean_path = os.path.join(settings.MEDIA_ROOT, 'data_clean.xlsx')
    output_path = settings.MEDIA_ROOT
    data_analysis = DataAnalysis(data_path, module_path, data_clean_path, output_path)
    if program == 'A':
        data_analysis.data_clean()
        data_analysis.data_copy()
    elif program == 'B':
        data_processB(data_path, module_path, output_path)


def download_fileA(request):
    path = os.path.join(settings.MEDIA_ROOT, 'A程序模板化.xlsx')
    file = open(path, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'aplication/octet-stream'
    response['COntentent-Disposition'] = 'attachment;filename="A程序模板化.xls"'
    return response


def download_fileB(request):
    path = os.path.join(settings.MEDIA_ROOT, 'B程序模板化.xlsx')
    file = open(path, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'aplication/octet-stream'
    response['COntentent-Disposition'] = 'attachment;filename="B程序模板化.xls"'
    return response
