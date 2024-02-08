from typing import Any
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import filesizeformat


@deconstructible
class RestrictedFileValidator:
    def __init__(self, content_types=None, max_size=None):
        """
        Initialize the RestrictedFileValidator

        Args:
            content_types (list, optional): List of allowed content types
            max_size (int, optional): Maximum file size in bytes
        """
        self.allowed_types = content_types or []
        self.max_size = max_size

    def __call__(self, file):
        """
        Performs validation on the uploaded file

        Args:
            file: The uploaded file object

        Raises:
            ValidationError: If the file type is not allowed exceeds the maximum size.
        """
        content_type = file.content_type
        if self.allowed_types and content_type not in self.allowed_types:
            raise ValidationError(f"'{content_type}' not supported.")
        if self.max_size and file.size > self.max_size:
            raise ValidationError(
                f"File size should not exceed {filesizeformat(self.max_size)}."
            )


class RestrictedFileField(models.FileField):
    def __init__(self, *args, **kwargs):
        """
        Initialize the RestrictedFileField

        Args:
            content_types (list, optional): List of allowed content types. If not specified,
            all content types are allowed.

            max_size (int, optional): Maximum file size in bytes. If not specified, no size
            is enforced.

        """
        self.content_types = kwargs.pop("content_types", None)
        self.max_size = kwargs.pop("max_size", None)
        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        """
        Perform validation on the field's value

        Args:
            value: The value of the field
            model_instance: The model instance containing the field.

        Raises:
            ValidationError: If the value fails validation.
        """
        super().validate(value, model_instance)
        if value:
            RestrictedFileValidator(self.content_types, self.max_size)(value.file)
