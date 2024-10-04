from rest_framework import serializers
from .models import Goods, Comment, Cart, CartItem


class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ['id', 'name', 'description', 'price', 'stock', 'image', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['user', 'goods', 'content', 'created_at']


class CartItemSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = CartItem
        fields = ['goods', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cartitem_set', many=True)

    class Meta:
        model = Cart
        fields = ['items']
