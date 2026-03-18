from rest_framework import serializers
from .models import Evento, Iscrizione, Utente


class UtenteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    class Meta:
        model = Utente
        fields = ["id", "email", "first_name", "last_name", "password", "ruolo", "is_staff", "is_active"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = Utente(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = "__all__"

class IscrizioneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Iscrizione
        fields = "__all__"

    def validate(self, data):
        request = self.context.get("request")
        user = request.user
        evento = data.get("evento")

        if user.ruolo == "organizzatore":
            utente = data.get("utente")
            if not utente:
                raise serializers.ValidationError({
                    "utente": "L'utente è obbligatorio."
                })
        else:
            utente = user

        queryset = Iscrizione.objects.filter(utente=utente, evento=evento)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError({
                "message": "Questo utente è già iscritto a questo evento."
            })

        return data