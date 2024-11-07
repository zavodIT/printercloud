# myapp/views.py
from django.shortcuts import redirect
from django.conf import settings
from urllib.parse import urlencode
import requests
from jose import jwt


def login(request):
    # Redirect to index if user is already authenticated
    if request.session.get('user'):
        return redirect(request.GET.get('next', '/'))

    # Build the Auth0 authorization URL with the "next" parameter if it exists
    next_url = request.GET.get('next', '/')
    auth0_url = f"https://{settings.AUTH0_DOMAIN}/authorize"
    params = {
        "response_type": "code",
        "client_id": settings.AUTH0_CLIENT_ID,
        "redirect_uri": settings.AUTH0_CALLBACK_URL,
        "scope": "openid profile email",
        "state": next_url  # Store the next URL in the state parameter
    }
    url = f"{auth0_url}?{urlencode(params)}"
    return redirect(url)

# myapp/views.py
import requests
from jose import jwt
from django.conf import settings
from django.shortcuts import redirect
from urllib.parse import urlencode

def get_auth0_jwks():
    jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
    jwks = requests.get(jwks_url).json()
    return jwks


def callback(request):
    code = request.GET.get('code')
    next_url = request.GET.get('state', '/')
    token_url = f"https://{settings.AUTH0_DOMAIN}/oauth/token"
    token_payload = {
        'client_id': settings.AUTH0_CLIENT_ID,
        'client_secret': settings.AUTH0_CLIENT_SECRET,
        'redirect_uri': settings.AUTH0_CALLBACK_URL,
        'code': code,
        'grant_type': 'authorization_code',
    }
    token_info = requests.post(token_url, json=token_payload).json()
    id_token = token_info.get("id_token")

    try:
        jwks = get_auth0_jwks()
        unverified_header = jwt.get_unverified_header(id_token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }

        if rsa_key:
            payload = jwt.decode(
                id_token,
                rsa_key,
                algorithms=["RS256"],
                audience=settings.AUTH0_CLIENT_ID,
                issuer=f"https://{settings.AUTH0_DOMAIN}/"
            )
            # Check if payload contains expected data
            print("Decoded payload:", payload)

            # Store user information in the session
            request.session['user'] = {
                'id': payload['sub'],
                'name': payload['name'],
                'email': payload['email'],
                'picture': payload.get('picture', '')
            }
            print("User session set:", request.session['user'])
            return redirect(next_url)
    except jwt.JWTError as e:
        print(f"JWT decoding error: {e}")
        return redirect('/login')

def logout(request):
    # Clear the session
    request.session.flush()

    # Build the logout URL to redirect to Auth0's logout endpoint
    logout_url = f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
    params = {
        "returnTo": "http://localhost:8000/",  # Redirect here after logging out
        "client_id": settings.AUTH0_CLIENT_ID
    }
    logout_redirect_url = logout_url + urlencode(params)
    return redirect(logout_redirect_url)