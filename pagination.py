from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from constants import S_PAGE_SIZE, M_PAGE_SIZE, L_PAGE_SIZE, XL_PAGE_SIZE
import math

class BasePagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = XL_PAGE_SIZE

    def get_paginated_response(self, data):
        total_items = self.page.paginator.count
        page_size = self.get_page_size(self.request)
        total_pages = math.ceil(total_items / page_size) if page_size else 1

        return Response({
            'count': total_items,
            'total_pages': total_pages,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

class SmallPagination(BasePagination):
    page_size = S_PAGE_SIZE

class MediumPagination(BasePagination):
    page_size = M_PAGE_SIZE

class LargePagination(BasePagination):
    page_size = L_PAGE_SIZE

class ExtraLargePagination(BasePagination):
    page_size = XL_PAGE_SIZE