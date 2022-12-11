from rest_framework import routers
from django.urls import path
from .views import TextingListViewSet, ClientViewSet, MessageViewSet, Test


router = routers.DefaultRouter()
router.register('texting-lists', TextingListViewSet)
router.register('clients', ClientViewSet)
router.register('messages', MessageViewSet)


urlpatterns = [
    path('tests/', Test.as_view(), name='test')
]

urlpatterns += router.urls
