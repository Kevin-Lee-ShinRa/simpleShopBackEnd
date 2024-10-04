"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from viewself.views import AuthorView, AuthorDetailView, PublishView, PublishDetailView

from myapp import views

from useapp import views

# from drfdemo import views

from drfdemo import views as drfdemo_views

# from drfdemo.views import StudentView, StudentDetailView
from drfdemo.views import StudentViewSet

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('index/', views.index),
    # path('user/list/', views.user_list),
    # path('user/add/', views.user_add),
    # path('user/something/', views.something),
    # path('login/', views.login),
    # path('orm/', views.orm),
    # path('info/list/', views.info_list),
    # path('info/add/', views.info_add),
    # path('info/delete/', views.info_delete),
    # new
    # 部门
    path('depart/list/', views.depart_list),
    path('depart/add/', views.depart_add),
    path('depart/delete/', views.depart_delete),
    # path('depart/edit/', views.depart_edit),
    path('depart/<int:nid>/edit/', views.depart_edit),
    # 用户

    path('user/list/', views.myuser_list),
    path('user/add/', views.myuser_add),
    path('user/add/model/', views.myuser_add_model),
    path('user/<int:nid>/edit/', views.myuser_edit),
    path('user/<int:nid>/delete/', views.myuser_delete),

    # path('pretty/list/', views.pretty_list),

    # drf http://127.0.0.1:8000/drfdemo/students/ get
    # path('student/', drfdemo_views.StudentView.as_view(), name='student'),
    # re_path('student/(\d+)/', drfdemo_views.StudentDetailView.as_view()),
    path("drfdemo/", include("drfdemo.urls")),

    # viewself
    path("authors/", AuthorView.as_view()),
    re_path("authors/(\d+)", AuthorDetailView.as_view()),
    path("publishes", PublishView.as_view()),
    re_path("publishes/(?P<pk>\d+)", PublishDetailView.as_view()),
]
