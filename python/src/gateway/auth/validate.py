import os, requests

def token(request):
    if not request.headers.get("Authorization"):
        return None, ("missing credentials", 401)
    
    token = request.headers.get("Authorization")

    if not token:
        return None, ("missing credentials", 401)
    
    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate",
        headers={"Authorization": token},
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
    