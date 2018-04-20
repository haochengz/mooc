
from random import choice


from django.core.mail import send_mail


from users.models import EmailVerify
from mooc.settings import EMAIL_FROM


test_server_addr = "http://127.0.0.1/"


def send_register_verify_mail(user):
    code = _generate_random_code()
    email_record = EmailVerify(
        email=user.email,
        code=code,
        verify_type="register"
    )
    email_record.save()
    subject = "Mooc verify mail"
    text = """
            Please click the link below to activate your account:
            %s%s%s
            
            If you cannot click that link, you could also copy that link and paste in the address bar of your browser.
        """ % (test_server_addr, "activate/", code)
    return _send_the_mail(user.email, subject, text)


def _generate_random_code(n=32):
    upper = [chr(x) for x in range(ord('A'), ord('A')+26)]
    lower = [chr(x) for x in range(ord('a'), ord('a')+26)]
    digit = [chr(x) for x in range(ord('0'), ord('0')+10)]
    base = upper + lower + digit
    gens = []

    for _ in range(n):
        gens.append(choice(base))

    return "".join(gens)


def _generate_text():
    pass


def _send_the_mail(email_addr, subject, text):
    return send_mail(subject=subject, message=text, from_email=EMAIL_FROM, recipient_list=[email_addr, ])
