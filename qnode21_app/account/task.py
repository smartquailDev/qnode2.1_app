from celery import Celery
from django.core.mail import send_mail , EmailMessage 
from django.template.loader import render_to_string
from django.conf import settings
from .models import Profile
from django.http import HttpResponse
from io import BytesIO
import weasyprint

#app=Celery('tasks', backend='rpc://guest:guest@rabbitmq:5672/', broker='pyamqp://guest:guest@rabbitmq:5672/')
app=Celery()

@app.task
def exams_results_create(profile_id):
    """
    Task para enviar una notificacion de terminado el examen por el Estudiante
    """
    profile = Profile.objects.get(id=profile_id)
    subject = 'Profile nr. {}'.format(profile.id)
    message = 'Estimado {}, \n\n Ha enviado correctamente su examen, a la escuela Manejo Seguro. Su codigo de examen es {}.'.format( profile.name, profile.id)
    email = EmailMessage(subject, message ,'smartquail.info@gmail.com',[profile.email])
    html = render_to_string('account/admin/profile/pdf.html', {'profile': profile})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=profile_{}.pdf"'.format(profile.id)
    out = BytesIO()
    weasyprint.HTML(string=html).write_pdf(out,response,stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/pdf.css')], presentational_hints=True)
    email.attach('profile_{}.pdf'.format(profile.id),out.getvalue(), 'application/pdf')
    return email.send()
