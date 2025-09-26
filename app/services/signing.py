import time, hmac, hashlib, base64, os

SECRET = os.getenv('SIGN_SECRET', 'devsecret')


def sign_path(path: str, ttl_sec: int = 300) -> str:
    '''Вернёт query-параметры exp и sig для подписи'''
    exp = int(time.time()) + ttl_sec
    msg = f'{path}:{exp}'.encode()
    sig = hmac.new(SECRET.encode(), msg, hashlib.sha256).digest()
    b64 = base64.urlsafe_b64encode(sig).decode().rstrip('=')
    return f'{path}?exp={exp}&sig={b64}'


def verify_path(path: str, exp: int, sig: str) -> bool:
    '''Проверка подписи'''
    msg = f'{path}:{exp}'.encode()
    expected = hmac.new(SECRET.encode(), msg, hashlib.sha256).digest()
    b64 = base64.urlsafe_b64encode(expected).decode().rstrip('=')
    return (b64 == sig) and (time.time() < exp)