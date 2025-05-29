import django_filters
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from app.api.services.create_eq import create_equipment_batch
from app.api.services.delete_eq import delete_equipment
from app.api.services.update_eq import update_equipment
from app.filters import EquipmentFilter
from app.models import Equipment, EquipmentType
from .serializers import EquipmentSerializer, EquipmentTypeSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny


class CustomPagination(PageNumberPagination):
    """Кастомная пагинация для DTO"""
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            "type": "equipment_list",
            "count": self.page.paginator.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "items": data
        })


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.filter(is_active=True)
    serializer_class = EquipmentSerializer
    filterset_class = EquipmentFilter
    search_fields = ['serial_number', 'comment', 'eq_type__name']
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
    ]
    pagination_class = CustomPagination
    
    def list(self, request, *args, **kwargs):
        """DTO формат"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "type": "equipment_list",
            "count": len(serializer.data),
            "items": serializer.data
        })

    def create(self, request, *args, **kwargs):
        """Метод для создания, логика вынесена в сервис"""
        data = request.data

        if not isinstance(data, list):
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response({
                "type": "equipment",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        created_objs, errors = create_equipment_batch(data)
        serialized = EquipmentSerializer(created_objs, many=True).data
        return Response({
            "type": "equipment_batch",
            "created": serialized,
            "errors": errors
        }, status=status.HTTP_207_MULTI_STATUS)

    def update(self, request, *args, **kwargs):
        """Метод для обновления, логка вынесена в отдельный сервис"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated = update_equipment(instance, serializer.validated_data)
        return Response({
            "type": "equipment",
            "data": self.get_serializer(updated).data
        })
        
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "type": "equipment",
            "data": serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        """Метод для удаления, логка вынесена в отдельный сервис"""
        instance = self.get_object()
        delete_equipment(instance)
        return Response({
            "type": "equipment",
            "status": "deleted",
            "id": instance.id
        }, status=status.HTTP_200_OK) 


class EquipmentTypePagination(PageNumberPagination):
    """Кастомная пагинация для DTO"""
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            "type": "equipment_type_list",
            "count": self.page.paginator.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "items": data
        })
        

class EquipmentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EquipmentType.objects.all()
    serializer_class = EquipmentTypeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    pagination_class = EquipmentTypePagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "type": "equipment_type_list",
            "count": len(serializer.data),
            "items": serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "type": "equipment_type",
            "data": serializer.data
        })


class LoginView(TokenObtainPairView):
    """Так как в проекте по умолчанию все запросы защищены аунтификацией, я переопределил вью для допуска в логину всех пользователей"""
    permission_classes = [AllowAny]