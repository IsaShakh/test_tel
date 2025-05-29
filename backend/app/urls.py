from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.api.views import EquipmentViewSet, EquipmentTypeViewSet, LoginView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register('equipment', EquipmentViewSet, basename='equipment')
router.register('equipment-type', EquipmentTypeViewSet, basename='equipment-type')

urlpatterns = [
    path('', include(router.urls)),  
    path('user/login/', LoginView.as_view(), name='token_obtain_pair'),
    path('user/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]