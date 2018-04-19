
from random import choice


def send_register_verify_mail(user):
    email_add = user.email


def send_forget_verify_mail(user):
    pass


def _generate_random_code(n=32):
    upper = [chr(x) for x in range(ord('A'), ord('A')+26)]
    lower = [chr(x) for x in range(ord('a'), ord('a')+26)]
    digit = [chr(x) for x in range(ord('0'), ord('0')+10)]
    base = upper + lower + digit
    gens = []

    for _ in range(n):
        gens.append(choice(base))

    return "".join(gens)


def _send_the_mail(text):
    pass
