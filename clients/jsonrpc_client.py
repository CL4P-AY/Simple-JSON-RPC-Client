import json
import ssl
import urllib.request
import tempfile
import uuid
from django.conf import settings


def call_jsonrpc_method(method_name, params=None, request_id=None):
    if params is None:
        params = {}
    if request_id is None:
        request_id = str(uuid.uuid4())

    payload = {
        "jsonrpc": "2.0",
        "method": method_name,
        "params": params,
        "id": request_id,
    }
    data = json.dumps(payload).encode("utf-8")

    with tempfile.NamedTemporaryFile(
        delete=False
    ) as cert_file, tempfile.NamedTemporaryFile(delete=False) as key_file:

        cert_file.write(settings.JSONRPC_CLIENT_CRT.encode("utf-8"))
        key_file.write(settings.JSONRPC_CLIENT_KEY.encode("utf-8"))

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_cert_chain(certfile=cert_file.name, keyfile=key_file.name)

    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED

    req = urllib.request.Request(
        url=settings.JSONRPC_ENDPOINT,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, context=context) as response:
            response_data = response.read().decode("utf-8")
            json_response = json.loads(response_data)
    except Exception as e:
        raise RuntimeError(
            f"An error occurred while executing JSON-RPC request: {e}"
        ) from e
    finally:
        pass

    if "error" in json_response:
        raise RuntimeError(f"JSON-RPC error: {json_response['error']}")

    return json_response
