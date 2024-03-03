from django.db import models


class SeparatedBinaryField(models.BinaryField):

    def __init__(self, *args, length=16, **kwargs):
        self.length = length
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.length != 16:
            kwargs["length"] = self.length
        return name, path, args, kwargs

    @property
    def non_db_attrs(self):
        return super().non_db_attrs + ("length",)

    def to_python(self, value):
        if isinstance(value, tuple) or isinstance(value, list):
            return value
        if value is None:
            return None
        return [value[i:i + self.length] for i in range(0, len(value), self.length)]

    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        return [value[i:i + self.length] for i in range(0, len(value), self.length)]

    def get_prep_value(self, value):
        return b''.join(value)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)


