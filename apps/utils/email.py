
from random import choice


from django.core.mail import send_mail
from django.core.exceptions import FieldError


from users.models import EmailVerify
from mooc.settings import EMAIL_FROM
from local import server_url


def send_register_verify_mail(user):
    code = generate_random_code()
    appears = EmailVerify.objects.filter(code=code)
    if len(appears) != 0:
        raise FieldError("unexpected random_code function produced same codes")
    email_record = EmailVerify(
        email=user.email,
        code=code,
        verify_type="register"
    )
    email_record.save()
    return _send_the_mail(user.email, *generate_register_mail(code))


def send_retrieve_password_mail(user):
    code = generate_random_code()
    appears = EmailVerify.objects.filter(code=code)
    if len(appears) != 0:
        raise FieldError("unexpected random_code function produced same codes")
    email_record = EmailVerify(
        email=user.email,
        code=code,
        verify_type="forget"
    )
    email_record.save()
    return _send_the_mail(user.email, *generate_retrieve_mail(code))


def generate_random_code(n=32):
    upper = [chr(x) for x in range(ord('A'), ord('A')+26)]
    lower = [chr(x) for x in range(ord('a'), ord('a')+26)]
    digit = [chr(x) for x in range(ord('0'), ord('0')+10)]
    base = upper + lower + digit
    gens = []

    for _ in range(n):
        gens.append(choice(base))

    return "".join(gens)


def generate_register_mail(code):
    subject = "Mooc verify mail"
    text = """
            Please click the link below to activate your account:
            %s
            
            If you cannot click that link, you could also copy that link and paste in the address bar of your browser.
            
            This validation code only validate within 30 minutes after it send out. So, make sure you click the link
            as soon as you can, if you accidentally gone out of date, you can hit the link below and retrieve a new
            validation code for your account. The new validation code could send every 30 minutes period.
        """ % generate_verify_url(code)
    return subject, text


def generate_retrieve_mail(code):
    subject = "Mooc verify mail, follow this procedure to retrieve your password"
    text = """
            Please click the link below to retrieve your password:
            %s
            
            If you cannot click that link, you could also copy that link and paste in the address bar of your browser.
            
            This validation code only validate within 30 minutes after it send out. So, make sure you click the link
            as soon as you can, if you accidentally gone out of date, you can hit the link below and retrieve a new
            validation code for your account. The new validation code could send every 30 minutes period.
        """ % generate_retrieve_url(code)
    return subject, text


def generate_verify_url(code):
    return server_url + "user/activate/" + code + "/"


def generate_retrieve_url(code):
    return server_url + "user/retrieve/" + code + "/"


def _send_the_mail(email_addr, subject, text):
    return send_mail(subject=subject, message=text, from_email=EMAIL_FROM, recipient_list=[email_addr, ])
