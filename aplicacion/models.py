from django.db import models
from django.contrib.auth.models import User

class CentroMedico(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Especialista(models.Model):
    nombre = models.CharField(max_length=255)
    especialidad = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nombre} - {self.especialidad}"

class Agenda(models.Model):
    fecha_disponible = models.DateField()
    hora_disponible = models.TimeField()
    especialista = models.ForeignKey(Especialista, on_delete=models.CASCADE)
    centro_medico = models.ForeignKey(CentroMedico, on_delete=models.CASCADE)

    def __str__(self):
        return f"Agenda {self.fecha_disponible} {self.hora_disponible} - {self.especialista} en {self.centro_medico}"

class Cita(models.Model):
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mensaje = models.TextField()

    def __str__(self):
        return f"Cita con {self.agenda.especialista} el {self.agenda.fecha_disponible} para {self.usuario.username}"

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

class Perfil(models.Model):
    USUARIO_TIPOS = (
        ('administrador', 'Administrador'),
        ('paciente', 'Paciente'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=20, choices=USUARIO_TIPOS, default='paciente')

    def __str__(self):
        return f'{self.user.username} - {self.tipo_usuario}'