from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Goods, Cart, Comment
from django.contrib.auth.models import User
from .serializers import GoodsSerializer, CommentSerializer, CartSerializer


# 商品列表视图
class GoodsListView(APIView):
    def get(self, request):
        goods = Goods.objects.all()
        serializer = GoodsSerializer(goods, many=True)
        return Response(serializer.data)


# 添加商品评论
class AddCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, goods_id):
        goods = Goods.objects.get(id=goods_id)
        content = request.data.get('content')
        comment = Comment.objects.create(user=request.user, goods=goods, content=content)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 用户购物车视图
class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        goods_id = request.data.get('goods_id')
        quantity = request.data.get('quantity', 1)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        goods = Goods.objects.get(id=goods_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, goods=goods)
        cart_item.quantity = quantity
        cart_item.save()
        return Response({'message': '商品已添加到购物车'}, status=status.HTTP_201_CREATED)
