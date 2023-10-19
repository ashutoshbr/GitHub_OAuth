import httpx
from fastapi import FastAPI
from starlette.responses import RedirectResponse

app = FastAPI()

# Obtained at OAuth portal of GitHub
CLIENT_ID = ""
CLIENT_SECRET = ""


@app.get("/github_login")
def github_login():
    # Redirect user for authorization at registered app (GitHub: Authorization Server)
    return RedirectResponse(
        f"https://github.com/login/oauth/authorize?client_id={CLIENT_ID}"
    )


@app.get("/github_code")
def github_code(code: str):
    # Authorization code given by GitHub can be exchanged for access_token
    # Exchange happens in back channel
    # Client ID and Client Secret along with the authorization code needs to be sent to GitHub
    headers = {"Accept": "application/json"}
    params = {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "code": code}
    response = httpx.post(
        url="https://github.com/login/oauth/access_token",
        headers=headers,
        params=params,
    )
    response_json = response.json()
    access_token = response_json["access_token"]
    # Access token can be used to get access to resource owner's data within the scope defined
    headers = {"Authorization": f"Bearer {access_token}"}
    response = httpx.get("https://api.github.com/user", headers=headers)
    return response.json()
