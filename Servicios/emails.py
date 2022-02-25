from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from django.template.loader import get_template




def email_notificacion_cliente(servicio):
    '''Envia un mail al cliente con la informacion de la orden de servicio.'''

    template = get_template('email_notificacion_cliente.html')
    context = {
        'servicio':servicio,
        }
    content = template.render(context)
    email = EmailMultiAlternatives(
        'Actualización Estado de Orden en PhoneFixSystem',
        '',
        settings.EMAIL_HOST_USER,
        [servicio.cliente.email],
        
    )
    email.attach_alternative(content, 'text/html')
    email.send()
    return print('email enviado')