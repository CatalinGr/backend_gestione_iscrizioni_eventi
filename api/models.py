from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UtenteManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, is_admin=False):
        if not email:
            raise ValueError("Email obbligatoria")

        if not password:
            raise ValueError("Password obbligatoria")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_admin=is_admin,
            is_staff=False,
            is_active=True
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_admin=True
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user


class Utente(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Ruoli(models.TextChoices):
        DIPENDENTE = "dipendente", "Dipendente"
        ORGANIZZATORE = "organizzatore", "Organizzatore"

    ruolo = models.CharField(max_length=20, choices=Ruoli.choices, default=Ruoli.DIPENDENTE)

    objects = UtenteManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = "Utente"
        verbose_name_plural = "Utenti"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Evento(models.Model):
    titolo = models.CharField(max_length=120)
    data = models.DateField()
    descrizione = models.TextField()

    def __str__(self):
        return f"{self.titolo} - {self.data}"

class Iscrizione(models.Model):
    utente = models.ForeignKey(
        Utente,
        on_delete=models.CASCADE,
        related_name='iscrizioni'
    )
    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        related_name='iscrizioni'        
    )
    checkin = models.BooleanField(default=False) 
    ora_checkin = models.TimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['utente', 'evento'], name='unique_iscrizione_utente_evento')
        ]