from re import sub
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


def snake_case(string, separator="-"):
    return separator.join(
        sub(
            "([A-Z][a-z]+)", r" \1", sub("([A-Z]+)", r" \1", string.replace("-", " "))
        ).split()
    ).lower()


def convert_groups_to_snake_case(groups):
    return list(map(snake_case, map(lambda group: group.name, groups)))


def delete_file_field(filefield):
    if not filefield:
        return
    try:
        file = filefield.file
    except FileNotFoundError:
        pass
    else:
        filefield.storage.delete(file.name)


def validate_date_range(start_date_field, end_date_field):
    if start_date_field and end_date_field and end_date_field < start_date_field:
        raise ValidationError(
            {"end_date": _("End date cannot be before the start date.")}
        )
