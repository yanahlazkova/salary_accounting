from django import forms


class BaseHTMXForm(forms.Form):
    hx_target = "#main-content"
    hx_push_url = "true"
    hx_swap = "innerHTML"
    submit_label = "Зберегти"
    submit_class = "btn btn-primary"
