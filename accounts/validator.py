from django.core.exceptions import ValidationError
import os
def allow_only_image_validator(value):
    ext = os.path.splitext(value.name)[1] # value = path. example cover_image.jpg, cover_image is at index 0 and .jpg is at index 1
    print(ext)

    valid_extensitons = ['.png', '.jpg', '.jpeg']
    if not ext.lower() in valid_extensitons:
        raise ValidationError("unsupported file extension. allowed extensions: " + str(valid_extensitons))