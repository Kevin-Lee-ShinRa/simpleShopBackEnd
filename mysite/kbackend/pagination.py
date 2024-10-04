from rest_framework.pagination import PageNumberPagination


# 第一个分页类
class CartPagination(PageNumberPagination):
    page_size = 18  # 每页 5 条


# 第二个分页类
class AllGoodsPagination(PageNumberPagination):
    page_size = 12  # 每页 20 条
    page_size_query_param = 'page_size'
    max_page_size = 100
