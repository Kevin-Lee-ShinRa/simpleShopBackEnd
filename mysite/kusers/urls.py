#coding=utf-8
from django.conf.urls.static import static
from django.urls import path, re_path, include
from . import views
from .views import RegisterView, CustomAuthToken, LogoutView, ProfileAPIView, UserCartAPIView, ProfileUpdateAPIView, \
    GetUserProfileAPIView
from django.conf import settings



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profiles/', ProfileAPIView.as_view(), name='profile-list'),
    path('ucarts/', UserCartAPIView.as_view(), name='cart-list'),
    path('uhistory/', UserCartAPIView.as_view(), name='cart-list'),
    path('profileupdate/', ProfileUpdateAPIView.as_view(), name='profile-update'),
    path('getuserprofile/', GetUserProfileAPIView.as_view(), name='get-profile-update'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
