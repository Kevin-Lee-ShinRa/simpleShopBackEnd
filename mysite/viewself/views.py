# from django.shortcuts import render
#
# from rest_framework import serializers
#
# from rest_framework.views import APIView
#
# from viewself.models import Book, Publish, Author
#
# from rest_framework.response import Response
#
#
# class AuthorSerializers(serializers.Serializer):
#     name = serializers.CharField(max_length=32)
#     age = serializers.IntegerField()
#
#     def create(self, validated_data):
#         author_obj = Author.objects.create(**validated_data)
#
#         return author_obj
#
#     def update(self, instance, validated_data):
#         Author.objects.filter(pk=instance.pk).update(**validated_data)
#
#         return instance
#
#
# # Create your views here.
#
#
# class AuthorView(APIView):
#     def get(self, request):
#         authors = Author.objects.all()
#         serializer = AuthorSerializers(instance=authors, many=True)
#         return Response(serializer.data)
#
#     # http: // 127.0.0.1: 8000 / authors /
#
#     def post(self, request):
#         serializer = AuthorSerializers(data=request.data)
#         if serializer.is_valid():
#             print("serializer.validated_data", serializer.validated_data)
#             # author_obj = Author.objects.create(**serializer.validated_data)
#             serializer.save()
#             # save instance 有值update 无值creat
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#
#
# class AuthorDetailView(APIView):
#     # 单一资源查看http://127.0.0.1:8000/authors/7
#     def get(self, request, id):
#         author = Author.objects.get(pk=id)
#         serializer = AuthorSerializers(instance=author, many=False)
#
#         return Response(serializer.data)
#
#     def put(self, request, id):
#         author = Author.objects.get(pk=id)
#         serializer = AuthorSerializers(instance=author, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#
#     def delete(self, request, id):
#         Author.objects.get(pk=id).delete()
#         return Response()
#
#
# ##############################################################
# # class PublishSerializers(serializers.ModelSerializer):
# #     class Meta:
# #         model = Publish
# #         fields = '__all__'
# #
# #
# # class PublishView(APIView):
# #     def get(self, request):
# #         publish_list = Publish.objects.all()
# #         serializer = PublishSerializers(instance=publish_list, many=True)
# #         return Response(serializer.data)
# #
# #     # http: // 127.0.0.1: 8000 / authors /
# #
# #     def post(self, request):
# #         serializer = PublishSerializers(data=request.data)
# #         if serializer.is_valid():
# #             print("serializer.validated_data", serializer.validated_data)
# #             # author_obj = Author.objects.create(**serializer.validated_data)
# #             serializer.save()
# #             # save instance 有值update 无值creat
# #             return Response(serializer.data)
# #         else:
# #             return Response(serializer.errors)
# #
# #
# # class PublishDetailView(APIView):
# #     # 单一资源查看http://127.0.0.1:8000/authors/7
# #     def get(self, request, id):
# #         publish = Publish.objects.get(pk=id)
# #         serializer = PublishSerializers(instance=publish, many=False)
# #
# #         return Response(serializer.data)
# #
# #     def put(self, request, id):
# #         publish = Publish.objects.get(pk=id)
# #         serializer = PublishSerializers(instance=publish, data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data)
# #         else:
# #             return Response(serializer.errors)
# #
# #     def delete(self, request, id):
# #         Publish.objects.get(pk=id).delete()
# #         return Response()
# ########################################################################
#
# from rest_framework.generics import GenericAPIView
#
# from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, \
#     DestroyModelMixin
#
# # from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# #
# #
# # class PublishSerializers(serializers.ModelSerializer):
# #     class Meta:
# #         model = Publish
# #         fields = '__all__'
#
#
#         # class Yuan(GenericAPIView, ListModelMixin, CreateModelMixin):
#         #     def get(self, request):
#         #         return self.list(request)
#         #
#         #     def post(self, request):
#         #         return self.create(request)
#         #
#         #
#         # class PublishView(Yuan):
#         #     queryset = Publish.objects
#         #     serializer_class = PublishSerializers
#
#
# # class PublishView(ListCreateAPIView):
# #     queryset = Publish.objects
# #     serializer_class = PublishSerializers
# #
# #
# # class PublishDetailView(RetrieveUpdateDestroyAPIView):
# #     queryset = Publish.objects
# #     serializer_class = PublishSerializers
#
#
# ################################################
#
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
#
#
# class PublishSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Publish
#         fields = '__all__'
#
# class PublishView(ListCreateAPIView):
#     queryset = Publish.objects
#     serializer_class = PublishSerializers
#
#
# class PublishDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = Publish.objects
#     serializer_class = PublishSerializers