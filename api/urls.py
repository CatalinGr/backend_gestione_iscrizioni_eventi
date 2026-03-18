from django.urls import include, path
from .views import EventoViewSet, IscrizioneViewSet, MeView, UtenteViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('utenti', UtenteViewSet, basename="lista-utenti")
router.register('eventi', EventoViewSet, basename="lista-eventi")
router.register('iscrizioni', IscrizioneViewSet, basename="lista-iscrizioni")

urlpatterns = [
    path('', include(router.urls)),
    path("me/", MeView.as_view(), name="me"),
]