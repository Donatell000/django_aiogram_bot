import hashlib

from django.utils import timezone


def generate_pk() -> str:
    now = timezone.now().isoformat()
    raw = f"{now}-salt-string"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]
