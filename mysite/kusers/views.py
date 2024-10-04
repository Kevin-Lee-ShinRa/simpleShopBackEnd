from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from kbackend.models import Goods, Cart, Orders, History
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Profile, UserCart, UserOrder, Comment, UserOrderItem, UserHistory
from .serializers import ProfileSerializer, UserCartSerializer, UserHistorySerializer
from rest_framework.parsers import MultiPartParser, FormParser


# 序列化器
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User  # 或者CustomUser
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # 如果使用CustomUser，请改为CustomUser
        fields = ['id', 'username', 'email']


class GetUserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]  # 确保只有已登录用户可以访问

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        data = {
            'avatar': profile.avatar.url if profile.avatar else None,  # 获取头像 URL
            'nickname': profile.nickname,  # 获取昵称
            'balance': profile.balance  # 可选字段
        }
        return Response(data)


class ProfileUpdateAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)

        nickname = request.data.get('nickname')
        avatar = request.FILES.get('avatar')

        # 更新昵称
        if nickname:
            profile.nickname = nickname

        # 更新头像
        if avatar:
            profile.avatar = avatar

        profile.save()

        return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)


class ProfileAPIView(APIView):
    def get(self, request, format=None):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCartAPIView(APIView):
    def get(self, request, format=None):
        user = request.user
        carts = UserCart.objects.filter(user=user)
        serializer = UserCartSerializer(carts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        user = request.user  # 假设用户已经通过身份验证
        goods_id = request.data.get('goods_id')  # 从请求中获取商品 ID
        quantity = request.data.get('quantity', 1)  # 获取数量，默认为1

        try:
            goods = Goods.objects.get(id=goods_id)
        except Goods.DoesNotExist:
            return Response({'error': 'Goods not found'}, status=status.HTTP_404_NOT_FOUND)

        # 创建购物车条目
        cart, created = UserCart.objects.get_or_create(
            user=user,
            good_name=goods.good_name,
            good_price=goods.good_price,
            good_description=goods.good_description,
            good_image=goods.good_image,
            defaults={'quantity': quantity}
        )

        if not created:
            cart.quantity += quantity
            cart.save()

        return Response({'message': 'Goods added to cart successfully'}, status=status.HTTP_201_CREATED)

    def delete(self, request, format=None):
        user = request.user
        cart_id = request.data.get('id')  # 从请求中获取购物车条目的 ID

        try:
            cart_item = UserCart.objects.get(id=cart_id, user=user)
        except UserCart.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

        # 删除购物车条目
        cart_item.delete()

        return Response({'message': 'Cart item deleted successfully'}, status=status.HTTP_200_OK)


class UserHistoryAPIView(APIView):
    def get(self, request, format=None):
        user = request.user
        carts = UserHistory.objects.filter(user=user)
        serializer = UserHistorySerializer(carts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        user = request.user  # 假设用户已经通过身份验证
        goods_id = request.data.get('goods_id')  # 从请求中获取商品 ID
        quantity = request.data.get('quantity', 1)  # 获取数量，默认为1

        try:
            goods = Goods.objects.get(id=goods_id)
        except Goods.DoesNotExist:
            return Response({'error': 'Goods not found'}, status=status.HTTP_404_NOT_FOUND)

        # 创建购物车条目
        cart, created = UserCart.objects.get_or_create(
            user=user,
            good_name=goods.good_name,
            good_price=goods.good_price,
            good_description=goods.good_description,
            good_image=goods.good_image,
        )

        if not created:
            # cart.quantity += quantity
            cart.save()

        return Response({'message': 'Goods added to cart successfully'}, status=status.HTTP_201_CREATED)

    def delete(self, request, format=None):
        user = request.user
        history_id = request.data.get('id')  # 从请求中获取购物车条目的 ID

        try:
            cart_item = UserCart.objects.get(id=history_id, user=user)
        except UserCart.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

        # 删除购物车条目
        cart_item.delete()

        return Response({'message': 'Cart item deleted successfully'}, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()  # 或者CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])  # 或者CustomUser
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user  # 获取用户信息

        return Response({
            'token': token.key,
            'username': user.username  # 包括用户名在响应中
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'message': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)

        token_key = auth_header.split(' ')[1]  # 从 "Token <token>" 中提取 token

        try:
            token = Token.objects.get(key=token_key)
            token.delete()  # 删除 token
            return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
