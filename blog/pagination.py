from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        page_lim = self.request.query_params.get(self.page_size_query_param,self.page_size)
        if page_lim!=None:
            page_lim = int(page_lim)
            if page_lim < 0:
                raise ValidationError({'message':'Invalid limit'})

            if page_lim == 0:
                page_lim = 10

        return Response({
            'page_size': page_lim,
            'total_pages': self.page.paginator.num_pages,
            'current_page': int(self.page.number),
            'total_data': self.page.paginator.count,
            'results': data,
        })
