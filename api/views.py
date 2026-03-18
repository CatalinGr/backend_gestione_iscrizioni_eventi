from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
from django.utils import timezone

from .models import Evento, Iscrizione, Utente
from .serializers import EventoSerializer, IscrizioneSerializer, UtenteSerializer
from .permissions import IsOrganizzatore


class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all().order_by("data")
    serializer_class = EventoSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsOrganizzatore()]

class IscrizioneViewSet(viewsets.ModelViewSet):
    serializer_class = IscrizioneSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.ruolo == "organizzatore":
            return Iscrizione.objects.all()

        return Iscrizione.objects.filter(utente=user)

    def perform_create(self, serializer):
        user = self.request.user

        if user.ruolo == "dipendente":
            serializer.save(utente=user)
        else:
            serializer.save()
    
    def perform_update(self, serializer):
        user = self.request.user

        if user.ruolo == "dipendente":
            serializer.save(utente=user)
        else:
            serializer.save()

    @action(detail=True, methods=["post"])
    def checkin(self, request, pk=None):
        iscrizione = self.get_object()

        iscrizione.checkin = True
        iscrizione.ora_checkin = timezone.now().time()
        iscrizione.save()

        return Response({"message": "Check-in registrato"})

class UtenteViewSet(viewsets.ModelViewSet):
    queryset = Utente.objects.all().order_by("first_name")
    serializer_class = UtenteSerializer

    def get_permissions(self):
        return [IsOrganizzatore()]


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UtenteSerializer(request.user)
        return Response(serializer.data)