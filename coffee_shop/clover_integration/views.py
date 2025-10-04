import requests
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

def connect_clover(request):
    auth_url = (
        f"{settings.CLOVER_BASE_URL}/oauth/v2/authorize"
        f"?client_id={settings.CLOVER_APP_ID}"
        f"&response_type=code"
        f"&redirect_uri={settings.CLOVER_REDIRECT_URI}"
    )
    return HttpResponseRedirect(auth_url)

@csrf_exempt
def clover_callback(request):
    code = request.GET.get("code")
    merchant_id = request.GET.get("merchant_id")

    if not code:
        return HttpResponse("Missing authorization code", status=400)

    token_url = f"{settings.CLOVER_BASE_URL}/oauth/v2/token"
    payload = {
        "client_id": settings.CLOVER_APP_ID,
        "client_secret": settings.CLOVER_APP_SECRET,
        "code": code,
    }

    headers = {"Content-Type": "application/json"}

    r = requests.post(token_url, json=payload, headers=headers, timeout=10)
    if r.status_code != 200:
        return HttpResponse(f"Token exchange failed: {r.text}", status=400)

    token_data = r.json()
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")

    request.session["merchant_id"] = merchant_id
    request.session["access_token"] = access_token

    return JsonResponse({
        "merchant_id": merchant_id,
        "access_token": access_token,
        "refresh_token": refresh_token,
    })
