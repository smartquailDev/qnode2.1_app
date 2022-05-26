from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
#from phonenumber_field.modelfields import PhoneNumberField
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext_lazy as _
from courses_exams.models import Test


class Profile(models.Model):

    OPCIONES_TIPO = (
    ('R', 'Regular'),
    ('I', 'Intensivo'),
    ('E', 'Especial'),
    ('P', 'Practica'),
)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    date_of_inscription = models.DateField(_('Fecha de Inscripción'), null=True,blank=True)
    name = models.CharField(_('Nombres'),max_length= 200,null=True,blank=True)
    last_name = models.CharField(_('Apellidos'),max_length= 200,null=True,blank=True)
    CI = models.IntegerField(_('Número de Cedula'),null=True,blank=True)
    adress = models.CharField(_('Dirección'),max_length= 200,null=True,blank=True)
    email = models.EmailField(_('Correo Electrónico'),max_length=254,null=True,blank=True)
    tel =  models.BigIntegerField(_('Número de Telefono'),null=True,blank=True)
    cel =  models.BigIntegerField(_('Número de Celular'),null=True,blank=True)
    course_type  = models.CharField(_('Tipo de Curso a Tomar'),max_length=1, choices=OPCIONES_TIPO,null=True,blank=True)
    date_of_birth = models.DateField(_('Fecha de Nacimiento'), null=True)
    photo = models.ImageField(_('Foto de Perfil'),upload_to='users/%Y/%m/%d/', blank=True)


    def __str__(self):
        return 'Perfil para usuario {}'.format(self.name)

    def get_total_results(self):
        return sum(item.get_grade() for item in self.items.all())

    def get_total_trys(self):
        return sum(item.get_trys() for item in self.items.all())
    class Meta:
        ordering =('name',)
       # verbose_name = 'Perfil de Estudiante'
       # verbose_name_plural = 'Perfiles de Estudiantes'

class Exams_resultsItems(models.Model):
    profile = models.ForeignKey(Profile,related_name='items',on_delete=models.CASCADE)
    test = models.ForeignKey(Test,related_name='exams_results_items',on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10,decimal_places=2)
    correct = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_grade(self):
        return self.value
    def get_trys(self):
        return self.correct 


class Contact(models.Model):
    user_from = models.ForeignKey('auth.User',
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User',
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from,
                                      self.user_to)



