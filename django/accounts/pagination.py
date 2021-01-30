from rest_framework import pagination
from rest_framework.response import Response


class Pagination(pagination.PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        next_page = None
        if self.page.has_next():
            next_page = self.page.next_page_number()
        prev_page = None
        if self.page.has_previous():
            prev_page = self.page.previous_page_number()
        return Response(
            {
                "prev_page": prev_page,
                "current_page": self.page.number,
                "next_page": next_page,
                "total_pages": self.page.paginator.num_pages,
                "page_size": self.page_size,
                "count": self.page.paginator.count,
                "results": data,
            }
        )
