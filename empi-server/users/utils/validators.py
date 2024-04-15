from django.core.exceptions import ValidationError


def validate_acad_year(value) -> None:
    message = f"{value} is not a pair of integers separated by a / with the latter exactly one higher that the former"

    first_year, second_year = value.split("/", maxsplit=1)
    if not first_year.isnumeric() or not second_year.isnumeric():
        raise ValidationError(message)
    first_year, second_year = int(first_year), int(second_year)

    if first_year + 1 != second_year:
        raise ValidationError(message)
