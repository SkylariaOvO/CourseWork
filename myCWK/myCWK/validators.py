import os
from django.conf import settings
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    """ Restricts file uploads to allowed extensions specified in settings.py """
    ext = os.path.splitext(value.name)[1]
    allowed_extensions = getattr(settings, "ALLOWED_UPLOAD_EXTENSIONS", [])

    if ext.lower() not in allowed_extensions:
        raise ValidationError(f"File type {ext} is not allowed. Allowed types: {', '.join(allowed_extensions)}")
