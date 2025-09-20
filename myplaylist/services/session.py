from datetime import datetime

# Save the initial tokens in current session
def save_access_tokens(request, tokens):
    # Save access tokens in session
    request.session["access_token"] = tokens["access_token"]
    request.session["refresh_token"] = tokens["refresh_token"]
    request.session["expires_in"] =  datetime.now().timestamp() + tokens["expires_in"]

# Get tokens from this user session
def get_user_tokens(request):
    return {
        "access_token": request.session.get("access_token"),
        "refresh_token": request.session.get("refresh_token"),
        "expires_in": request.session.get("expires_in")
    }

# Check if token is expired
def is_expired(request):
    return datetime.now().timestamp() > request.session["expires_in"]

# Update tokens after refresh
def update_tokens(request, new_tokens):
        request.session["access_token"] = new_tokens["access_token"]
        request.session["expires_in"] = datetime.now().timestamp() + new_tokens["expires_in"]
