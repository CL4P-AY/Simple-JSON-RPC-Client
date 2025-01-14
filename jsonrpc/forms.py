from django import forms


class JsonRpcForm(forms.Form):
    method = forms.CharField(label="Method", max_length=100, required=True)
    params = forms.CharField(
        label="Params (JSON)",
        widget=forms.Textarea,
        required=False,
        initial="{}",
    )
