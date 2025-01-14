from django.urls import path
from jsonrpc.views import JsonRpcCallView

urlpatterns = [
    path("jsonrpc-call/", JsonRpcCallView.as_view(), name="jsonrpc-call"),
]
