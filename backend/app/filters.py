import django_filters
from app.models import Equipment


class EquipmentFilter(django_filters.FilterSet):
    type_id = django_filters.NumberFilter(field_name='type__id')
    type_name = django_filters.CharFilter(field_name='type__name', lookup_expr='icontains')
    serial_number = django_filters.CharFilter(lookup_expr='icontains')
    comment = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Equipment
        fields = ['type_id', 'type_name', 'serial_number', 'comment']
