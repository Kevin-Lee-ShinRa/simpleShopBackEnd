from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from kbackend.models import Goods, Cart, Orders, History, Comment, Reply
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .pagination import AllGoodsPagination, CartPagination


# 序列化器
class CommentSerializer(serializers.ModelSerializer):
    commenter_name = serializers.CharField(source='commenter.username', read_only=True)
    commenter_nickname = serializers.CharField(source='commenter.profile.nickname', read_only=True)
    commenter_avatar = serializers.ImageField(source='commenter.profile.avatar', read_only=True)
    replies = serializers.SerializerMethodField()
    goods = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'goods', 'commenter_name', 'commenter_avatar', 'content', 'created_at', 'replies',
                  'commenter_nickname']

    def get_replies(self, obj):
        replies = obj.replies.all()
        return ReplySerializer(replies, many=True).data


class ReplySerializer(serializers.ModelSerializer):
    replier_name = serializers.CharField(source='replier.profile.nickname', read_only=True)
    replier_avatar = serializers.ImageField(source='replier.profile.avatar', read_only=True)
    comment = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Reply
        fields = ['id', 'comment', 'replier_name', 'replier_avatar', 'content', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # 如果使用CustomUser，请改为CustomUser
        fields = ['id', 'username', 'email']


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


class GoodsSerializers(serializers.ModelSerializer):
    uploader_id = serializers.ReadOnlyField(source='uploader.id')
    uploader_avatar = serializers.ImageField(source='uploader.profile.avatar', read_only=True)
    uploader_nickname = serializers.CharField(source='uploader.profile.nickname', read_only=True)

    class Meta:
        model = Goods
        fields = '__all__'
        read_only_fields = ['uploader']


class CartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class OrdersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


class HistorySerializers(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'


class CommentsAPIView(APIView):
    # 未登录的用户可以查看评论
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]  # 允许所有用户进行GET请求
        return [IsAuthenticated()]  # 其他请求需要登录

    def get(self, request, goods_id):
        # 获取商品并查询该商品的所有评论
        goods = get_object_or_404(Goods, id=goods_id)
        comments = goods.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, goods_id):
        # 添加评论，确保用户已登录
        goods = get_object_or_404(Goods, id=goods_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            # 保存评论，并自动附带商品和评论者
            serializer.save(goods=goods, commenter=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, comment_id):
        # 更新评论，确保是评论的作者
        comment = get_object_or_404(Comment, id=comment_id, commenter=request.user)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        # 删除评论，确保是评论的作者
        comment = get_object_or_404(Comment, id=comment_id, commenter=request.user)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReplyAPIView(APIView):
    # 未登录用户可以查看回复，登录用户可以添加、修改和删除回复
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]  # POST、PUT、DELETE 需要登录

    def get(self, request, comment_id):
        """获取指定评论的所有回复"""
        comment = get_object_or_404(Comment, id=comment_id)
        replies = comment.replies.all()
        serializer = ReplySerializer(replies, many=True)
        return Response(serializer.data)

    def post(self, request, comment_id):
        """为某个评论添加回复"""
        comment = get_object_or_404(Comment, id=comment_id)
        serializer = ReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(comment=comment, replier=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, reply_id):
        """修改自己的回复"""
        reply = get_object_or_404(Reply, id=reply_id, replier=request.user)
        serializer = ReplySerializer(reply, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, reply_id):
        """删除自己的回复"""
        reply = get_object_or_404(Reply, id=reply_id, replier=request.user)
        reply.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class GoodsView(GenericAPIView):
    permission_classes = [AllowAny]
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializers
    pagination_class = AllGoodsPagination

    def get(self, request):
        # 获取搜索关键字
        search_query = request.query_params.get('search', '')

        # 获取排序方式：可以是 'date_asc', 'date_desc', 'price_asc', 'price_desc'
        order_by = request.query_params.get('sort', '')

        # 根据搜索关键字过滤商品
        queryset = self.get_queryset()
        if search_query:
            queryset = queryset.filter(good_name__icontains=search_query)

        # 根据排序方式进行排序
        if order_by == 'date_asc':
            queryset = queryset.order_by('created_at')  # 日期升序
        elif order_by == 'date_desc':
            queryset = queryset.order_by('-created_at')  # 日期降序
        elif order_by == 'price_asc':
            queryset = queryset.order_by('good_price')  # 价格升序
        elif order_by == 'price_desc':
            queryset = queryset.order_by('-good_price')  # 价格降序

        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # 如果没有分页
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uploader=request.user)
            return Response(serializer.data)
        else:
            print("Serializer errors:", serializer.errors)  # 打印错误信息
            return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            goods = self.get_queryset().get(pk=pk)  # 根据ID获取商品
            goods.delete()  # 删除商品
            return Response(status=status.HTTP_204_NO_CONTENT)  # 返回204状态表示删除成功
        except Goods.DoesNotExist:
            return Response({"detail": "Goods not found."}, status=status.HTTP_404_NOT_FOUND)  # 商品未找到时返回404状态


class GoodsDetailView(GenericAPIView):
    queryset = Goods.objects
    serializer_class = GoodsSerializers

    def get(self, request, pk):
        serializer = self.get_serializer(instance=self.get_object(), many=False)

        return Response(serializer.data)

    def put(self, request, pk):
        serializer = self.get_serializer(instance=self.get_object(), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object().delete()
        return Response()


class CartView(GenericAPIView):
    queryset = Cart.objects
    serializer_class = CartSerializers

    def get(self, request):
        # serializer = self.serializer_class(instance=self.queryset, many=True)
        # serializer = self.get_serializer(instance=self.queryset, many=True)
        serializer = self.get_serializer(instance=self.get_queryset(), many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            print("serializer.validated_data", serializer.validated_data)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class CartDetailView(GenericAPIView):
    queryset = Cart.objects
    serializer_class = CartSerializers

    def get(self, request, pk):
        serializer = self.get_serializer(instance=self.get_object(), many=False)

        return Response(serializer.data)

    def put(self, request, pk):
        serializer = self.get_serializer(instance=self.get_object(), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object().delete()
        return Response()


class OrdersView(GenericAPIView):
    queryset = Orders.objects
    serializer_class = OrdersSerializers

    def get(self, request):
        # serializer = self.serializer_class(instance=self.queryset, many=True)
        # serializer = self.get_serializer(instance=self.queryset, many=True)
        serializer = self.get_serializer(instance=self.get_queryset(), many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            print("serializer.validated_data", serializer.validated_data)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class OrdersDetailView(GenericAPIView):
    queryset = Orders.objects
    serializer_class = OrdersSerializers

    def get(self, request, pk):
        serializer = self.get_serializer(instance=self.get_object(), many=False)

        return Response(serializer.data)

    def put(self, request, pk):
        serializer = self.get_serializer(instance=self.get_object(), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object().delete()
        return Response()


class HistoryView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HistorySerializers

    def get_queryset(self):
        # 过滤出当前用户的历史记录
        return History.objects.filter(user=self.request.user)

    def get(self, request):
        serializer = self.get_serializer(instance=self.get_queryset(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # 将当前用户信息添加到数据中
            serializer.save(user=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class HistoryDetailView(GenericAPIView):
    queryset = History.objects
    serializer_class = GoodsSerializers

    def get(self, request, pk):
        serializer = self.get_serializer(instance=self.get_object(), many=False)

        return Response(serializer.data)

    def put(self, request, pk):
        serializer = self.get_serializer(instance=self.get_object(), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object().delete()
        return Response()


from django.shortcuts import get_object_or_404


def add_to_cart(request, source_id):
    try:
        source_item = get_object_or_404(Goods, id=source_id)
        Cart.objects.create(
            good_name=source_item.good_name,
            good_price=source_item.good_price,
            good_image=source_item.good_image
        )
        return HttpResponse('Item added to cart successfully!')
    except Exception as e:
        return HttpResponse(f'Error occurred: {str(e)}', status=500)


def add_to_orders(request, source_id):
    try:
        source_item = get_object_or_404(Cart, id=source_id)
        Orders.objects.create(
            good_name=source_item.good_name,
            good_price=source_item.good_price,
            good_image=source_item.good_image
        )
        return HttpResponse('Item added to orders successfully!')
    except Exception as e:
        return HttpResponse(f'Error occurred: {str(e)}', status=500)


def goods_to_history(request, source_id):
    try:
        source_item = get_object_or_404(Goods, id=source_id)
        History.objects.create(
            good_name=source_item.good_name,
            good_price=source_item.good_price,
            good_image=source_item.good_image
        )
        return HttpResponse('Item added to orders successfully!')
    except Exception as e:
        return HttpResponse(f'Error occurred: {str(e)}', status=500)
