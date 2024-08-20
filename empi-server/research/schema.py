from drf_spectacular.extensions import OpenApiAuthenticationExtension


class ResearchAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'research.auth.ResearchAuthentication'  # full import path OR class ref
    name = 'ResearchAuthentication'  # name used in the schema

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'basic'
        }
