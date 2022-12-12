from rest_framework import routers
from .views import TextingListViewSet, ClientViewSet, MessageViewSet


router = routers.DefaultRouter()
router.register('texting-lists', TextingListViewSet)
router.register('clients', ClientViewSet)
router.register('messages', MessageViewSet)


urlpatterns = []

urlpatterns += router.urls
