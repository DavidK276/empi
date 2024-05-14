from django.db import models


class SeparatedValuesField(models.Field):

    def __init__(self, *args, field=models.Field, token=",", **kwargs):
        assert field is not None
        self.token = token
        self.field = field
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.token != ",":
            kwargs["token"] = self.token
        return name, path, args, kwargs

    def db_type(self, connection):
        return "text"

    @property
    def non_db_attrs(self):
        return super().non_db_attrs + ("field",)

    def validate(self, values, model_instance):
        super().validate(values, model_instance)
        for value in values:
            for validator in self.field.default_validators:
                validator(value)

    def to_python(self, values):
        if isinstance(values, tuple) or isinstance(values, list):
            return values
        if values is None:
            return None
        return values.split(self.token)

    def from_db_value(self, values, expression, connection):
        if values is None:
            return None
        return values.split(self.token)

    def get_prep_value(self, values):
        if isinstance(values, str):
            return values
        return self.token.join(values)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)
