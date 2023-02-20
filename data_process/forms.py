from django import forms
from . import models
from django.core.exceptions import ObjectDoesNotExist


class UserInfoForm(forms.Form):
    numbers = forms.CharField(max_length=6, min_length=6, required=True,
                              error_messages={'required': '请输入账号',
                                              'max_length': '请输入正确的工号',
                                              'min_length': '请输入正确的工号'},
                              strip=True)
    password = forms.CharField(max_length=20, min_length=6,  required=True)


def clean_name(self):
    try:
        models.UserInfo.objects.get(name=self.numbers)
    except models.UserInfo.DoesNotExist:
        ValueError('不存在该用户')
    else:
        pass
