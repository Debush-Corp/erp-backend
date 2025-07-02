from django.core.paginator import EmptyPage
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from constants import S_PAGE_SIZE, M_PAGE_SIZE, L_PAGE_SIZE, XL_PAGE_SIZE
import math

from rest_framework.exceptions import NotFound

class BasePagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100  # reemplaza con XL_PAGE_SIZE si lo tienes definido

    def paginate_queryset(self, queryset, request, view=None):
        self.request = request
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)

        try:
            self.page = paginator.page(page_number)
        except Exception:
            # Página no existe
            self.page = None
            self.paginator = paginator
            return []

        self.paginator = paginator
        return list(self.page)

    def get_paginated_response(self, data):
        total_items = self.paginator.object_list.count()
        page_size = self.get_page_size(self.request)
        num_pages = math.ceil(total_items / page_size) if page_size else 1

        if self.page is None:
            print(f"La pagina no existe, retornando total_page: {num_pages}")
            return Response({
                'total_items': total_items,
                'page_items': 0,
                'page_size': page_size,
                'total_pages': num_pages,
                'next': None,
                'previous': None,
                'results': [],
                'page_exists': False
            })

        page_items = self.page.paginator.count

        return Response({
            'total_items': total_items,
            'page_items': page_items,
            'page_size': page_size,
            'total_pages': num_pages,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
            'page_exists': True
        })

class SmallPagination(BasePagination):
    page_size = S_PAGE_SIZE

class MediumPagination(BasePagination):
    page_size = M_PAGE_SIZE

class LargePagination(BasePagination):
    page_size = L_PAGE_SIZE

class ExtraLargePagination(BasePagination):
    page_size = XL_PAGE_SIZE