from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_contact_email(name, email, subject, message):
    full_message = f"""
    You’ve received a new message from your blog contact form

    From: {name}
    Email: {email}

    Message:
    {message}
    """

    send_mail(
        subject=f"[My Blog Contact] {subject}",
        message=full_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['hithapersonalblog@gmail.com'],  # recipient mail
        fail_silently=False,
    )
