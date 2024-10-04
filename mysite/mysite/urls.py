from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from kbackend.views import GoodsView, GoodsDetailView, CartView, CartDetailView, OrdersView, OrdersDetailView, \
    add_to_cart, goods_to_history, add_to_orders, HistoryView, HistoryDetailView, RegisterView, CustomAuthToken, \
    LogoutView, CommentsAPIView, ReplyAPIView

urlpatterns = [
    path('addtocart/<int:source_id>/', add_to_cart, name='add_to_cart'),
    path('addtoorders/<int:source_id>/', add_to_orders, name='add_to_orders'),
    path('goodstohistory/<int:source_id>/', goods_to_history, name='goods_to_history'),
    path("allgoods/", GoodsView.as_view()),
    path('allgoods/<int:pk>/', GoodsView.as_view()),
    path("orders", OrdersView.as_view()),
    re_path("allgoods/(?P<pk>\d+)", GoodsView.as_view()),
    path("cart", CartView.as_view()),
    re_path("cart/(?P<pk>\d+)", CartDetailView.as_view()),
    path("history", HistoryView.as_view()),
    re_path("history/(?P<pk>\d+)", HistoryDetailView.as_view()),
    path('admin/', admin.site.urls),
    path('myloginpart/', include('kusers.urls')),
    # 评论
    path('goods/<int:goods_id>/comments/', CommentsAPIView.as_view(), name='comments-list'),
    path('comments/<int:comment_id>/replies/', ReplyAPIView.as_view(), name='replies-list'),
    path('comments/<int:comment_id>/', CommentsAPIView.as_view(), name='comment-detail'),
    path('replies/<int:reply_id>/', ReplyAPIView.as_view(), name='reply-detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)