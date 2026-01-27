class HTMXResponseMixin:

    htmx_template = None

    def get_template_names(self):
        if self.request.headers.get("HX-Request") and self.htmx_template:
            return [self.htmx_template]
        return super().get_template_names()
