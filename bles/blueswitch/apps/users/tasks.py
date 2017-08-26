from django.template import RequestContext, TemplateDoesNotExist
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def email_password_reset_link(user, password_reset_link):
    '''
    '''
    ctx_dict = {'password_reset_link': password_reset_link, 'user': user}

    subject = render_to_string('accounts/forgot_password_subject.txt', ctx_dict)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())

    message_txt = render_to_string('accounts/forgot_password_email.txt', ctx_dict)
    email_message = EmailMultiAlternatives(subject, message_txt, settings.DEFAULT_FROM_EMAIL, [user.email])

    try:
        message_html = render_to_string('accounts/forgot_password_email.html', ctx_dict)
    except TemplateDoesNotExist:
        message_html = None

    if message_html:
        email_message.attach_alternative(message_html, 'text/html')

    email_message.send()
