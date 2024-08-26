from drf_spectacular.extensions import OpenApiAuthenticationExtension


class KnoxAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "knox.auth.TokenAuthentication"  # full import path OR class ref
    name = "TokenAuthentication"  # name used in the schema

    def get_security_definition(self, auto_schema):
        return {"type": "http", "scheme": "bearer"}
