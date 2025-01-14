import json
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import JsonRpcForm
from clients.jsonrpc_client import call_jsonrpc_method


class JsonRpcCallView(FormView):
    template_name = "jsonrpc_form.html"
    form_class = JsonRpcForm
    success_url = reverse_lazy("jsonrpc-call")

    def form_valid(self, form):
        method = form.cleaned_data["method"]
        params_str = form.cleaned_data["params"]

        try:
            params_dict = json.loads(params_str)
        except json.JSONDecodeError:
            params_dict = {}

        try:
            result = call_jsonrpc_method(method, params=params_dict)
        except Exception as e:
            return self.render_to_response(
                self.get_context_data(form=form, error=str(e))
            )

        return self.render_to_response(
            self.get_context_data(
                form=form, result=json.dumps(result, indent=2, ensure_ascii=False)
            )
        )
