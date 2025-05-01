from django.core import signing

SALT    = 'email-verification'
MAX_AGE = 60 * 60 * 24  # 24h

def make_token(email: str) -> str:
    signer = signing.TimestampSigner(salt=SALT)
    return signer.sign(email)

def verify_token(token: str) -> str:
    signer = signing.TimestampSigner(salt=SALT)
    return signer.unsign(token, max_age=MAX_AGE)