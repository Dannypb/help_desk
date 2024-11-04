from django.urls import path, include
from rest_framework import routers
from api import views
from django.conf import settings
from django.conf.urls.static import static
from api.views import LoginViewSet, UserViewSet, ClientViewSet, OccupationViewSet, AgentViewSet, TicketViewSet

router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'client', ClientViewSet)
router.register(r'occupation', OccupationViewSet)
router.register(r'agent', AgentViewSet)
router.register(r'ticket', TicketViewSet)


urlpatterns  = [
    path('', include(router.urls)),
    path('login/', LoginViewSet.as_view(), name='login'),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)