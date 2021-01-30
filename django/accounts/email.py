from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import loader

from .apps import app_name


def send_mail(
    subject_template_name,
    email_template_name,
    context,
    from_email,
    to_email,
    html_email_template_name=None,
):
    subject = loader.render_to_string(subject_template_name, context)
    subject = "".join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)
    email_message = EmailMultiAlternatives(
        subject, body, from_email, [to_email]
    )
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, "text/html")
    email_message.send()


def get_sites_context(request=None):
    current_site = get_current_site(request)
    is_secure = request and request.is_secure()
    return {
        "frontend_origin": settings.FRONTEND_ORIGIN,
        "domain": current_site.domain,
        "site_name": current_site.name,
        "protocol": "https" if is_secure else "http",
    }


def password_reset_email(request, user):
    ctx = get_sites_context(request)
    ctx.update(
        {
            "user": user,
            "uid": user.url_encode(),
            "token": user.tokenize(),
        }
    )
    send_mail(
        f"{app_name}/password_reset_email/subject.txt",
        f"{app_name}/password_reset_email/body.txt",
        ctx,
        None,
        user.email,
    )
