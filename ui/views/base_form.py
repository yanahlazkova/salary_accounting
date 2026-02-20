from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic.edit import ModelFormMixin
from django.views.generic import View


class UIBaseFormView(ModelFormMixin, View):
    template_name = "ui/forms/base_form.html"
    success_url = None
    form_title = None

    def get(self, request, *args, **kwargs):
        self.object = None
        if hasattr(self, "get_object"):
            try:
                self.object = self.get_object()
            except Exception:
                self.object = None

        form = self.get_form()
        context = self.get_context_data(form=form)
        return self.render(context)

    def post(self, request, *args, **kwargs):
        self.object = None
        if hasattr(self, "get_object"):
            try:
                self.object = self.get_object()
            except Exception:
                self.object = None

        form = self.get_form()

        if form.is_valid():
            self.object = form.save()
            return self.form_valid_response()

        return self.form_invalid_response(form)

    # ---------------------

    def form_valid_response(self):
        response = HttpResponse()
        response["HX-Redirect"] = self.get_success_url()
        return response

    def form_invalid_response(self, form):
        context = self.get_context_data(form=form)
        return self.render(context)

    def render(self, context):
        html = render_to_string(
            self.template_name,
            context,
            request=self.request
        )
        return HttpResponse(html)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["toolbar_buttons"] = self.get_toolbar_buttons()
        return context

    def get_toolbar_buttons(self):
        return []
