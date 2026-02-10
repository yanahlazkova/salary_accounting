from dataclasses import dataclass, field
from typing import Dict, Optional
from django.urls import reverse


@dataclass
class HTMXButton:
    name: str
    label: str
    icon: str
    url_name: str
    url_kwargs: Dict[str, object] = field(default_factory=dict)

    css_class: str = "btn btn-outline-info"
    hx_method: str = "get"
    hx_target: str = "#main-content"
    hx_push_url: str = "true"
    hx_swap: str = "innerHTML"

    confirm: Optional[str] = None # текст підтвердження
    disabled: bool = False

    def url(self) -> str:
        return reverse(self.url_name, kwargs=self.url_kwargs)

    def htmx_attrs(self) -> Dict[str, str]:
        attrs = {
            f"hx-{self.hx_method}": self.url(),
            "hx-target": self.hx_target,
            "hx-push-url": self.hx_push_url,
            "hx-swap": self.hx_swap,
        }
        if self.confirm:
            attrs["hx-confirm"] = self.confirm
        return attrs
