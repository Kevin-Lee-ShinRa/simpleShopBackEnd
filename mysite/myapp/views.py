from django.shortcuts import render, redirect
from django.http import HttpResponse

from myapp.models import UserInfo


def index(request):
    return HttpResponse("欢迎使用")


def user_list(request):
    return render(request, "user_list.html")


def user_add(req):
    import requests
    res = requests.get("https://api.github.com/repos/octocat/Hello-World")
    data_list = res.json()
    print(data_list)
    return render(req, 'user_add.html')


def something(request):
    print(request.method)
    print(request.POST)
    # return HttpResponse("返回内容")

    return redirect("https://www.google.com")


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
        # else:
        username = request.POST.get("user")
        password = request.POST.get("userone")
        if username == 'root' and password == "123456":
            # print(request.POST)
            # return HttpResponse("登录成功")
            return redirect("......")
            # else:
            # return HttpResponse("登录失败")
            return render(request, "login.html", {"error_msg": "存在错误"})


from myapp import models


def orm(request):
    models.UserInfo.objects.filter(id=11).delete()

    return HttpResponse("成功")


def info_list(request):
    data_list = UserInfo.objects.all()
    print(data_list)

    return render(request, "info_list.html", {"data_list": data_list})


def info_add(request):
    if request.method == "GET":
        return render(request, "info_add.html")
    name = request.POST.get("name")
    password = request.POST.get("password")
    age = request.POST.get("age")

    UserInfo.objects.create(name=name, password=password, age=age)

    # return HttpResponse("添加成功")
    return redirect("/info/list/")


def info_delete(request):
    nid = request.GET.get("nid")
    UserInfo.objects.filter(id=nid).delete()
    return redirect("/info/list/")
