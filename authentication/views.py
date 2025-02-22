from django.http import JsonResponse
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
import json

User = get_user_model()


@csrf_exempt
def signup(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if not email or not username or not password:
        return JsonResponse({"error": "All fields are required"}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({"error": "Email already in use"}, status=400)

    user = User.objects.create(
        email=email,
        username=username,
        password=make_password(password)
    )

    user.generate_tokens()

    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return JsonResponse({
            "id": str(user.id),
            "email": user.email,
            "username": user.username,
            "access_token": user.access_token,
            "refresh_token": user.refresh_token
        }, status=201)

    return JsonResponse({"error": "Signup successful but auto-login failed"},
                        status=500)


@csrf_exempt
def signin(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return JsonResponse({"error": "All fields are required"}, status=400)

    user = authenticate(username=email, password=password)
    if user:
        login(request, user)
        return JsonResponse({
            "id": str(user.id),
            "email": user.email,
            "username": user.username,
            "access_token": user.access_token,
            "refresh_token": user.refresh_token
        }, status=200)

    return JsonResponse({"error": "Invalid credentials"}, status=401)
