from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class EquipmentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            "type": "equipment_list",
            "count": self.page.paginator.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "items": data,
        })
        
        
class EquipmentTypePagination(EquipmentPagination):
    def get_paginated_response(self, data):
        return Response({
            "type": "equipment_type_list",
            "count": self.page.paginator.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "items": data,
        })
