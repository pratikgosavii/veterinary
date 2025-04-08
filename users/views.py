from email import message
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from .forms import *


# def login_page(request):
#     forms = LoginForm()
#     if request.method == 'POST':
#         forms = LoginForm(request.POST)
#         if forms.is_valid():
#             username = forms.cleaned_data['username']
#             password = forms.cleaned_data['password']
#             print(username)
#             print(password)
#             user = authenticate(username=username, password=password)
#             if user:
#                 login(request, user)

#                 if user.is_doctor:
#                     print('---------------------------------')
#                     print('---------------------------------')
#                     print('---------------------------------')
#                 return redirect('dashboard')
#             else:
#                 messages.error(request, 'wrong username password')
#     context = {'form': forms}
#     return render(request, 'adminLogin.html', context)

from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class SignupView(APIView):

    def post(self, request):
        id_token = request.data.get("idToken")
        user_type = request.data.get("user_type")  # e.g. 'daycare', 'doctor', etc.

        if not id_token or not user_type:
            return Response({"error": "idToken and user_type are required"}, status=400)

        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            mobile = decoded_token.get("phone_number")

            uid = decoded_token["uid"]

            if not mobile:
                return Response({"error": "Phone number not found in Firebase token"}, status=400)

            # Set default role flags
            role_flags = {
                "is_customer": False,
                "is_doctor": False,
                "is_daycare": False,
                "is_service_provider": False
            }

            if f"is_{user_type}" not in role_flags:
                return Response({"error": "Invalid user_type"}, status=400)

            role_flags[f"is_{user_type}"] = True

            # Get or create user with appropriate role
            user, created = User.objects.get_or_create(
                mobile=mobile,
                uid=uid,
                defaults=role_flags
            )

            # If user existed and user_type doesn't match, you may reject or update
            if not created and not getattr(user, f"is_{user_type}"):
                return Response({"error": f"User already exists as different type"}, status=400)

            # Generate JWT
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "mobile": user.mobile,
                    "user_type": user_type,
                    "created": created
                }
            })

        except Exception as e:
            return Response({"error": str(e)}, status=400)

    

from firebase_admin import auth as firebase_auth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User  # Adjust as needed

class LoginAPIView(APIView):
    def post(self, request):
        id_token = request.data.get("id_token")

        if not id_token:
            return Response({"error": "ID token missing"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            uid = decoded_token["uid"]
            phone_number = decoded_token.get("phone_number")
            email = decoded_token.get("email")

            # Check if user exists
            user, created = User.objects.get_or_create(mobile=phone_number, defaults={
                "email": email or "",
                "username": phone_number
            })

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {"id": user.id, "mobile": user.mobile}
            })

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)



def  login_admin(request):

    forms = LoginForm()
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        if forms.is_valid():
            email = forms.cleaned_data['email']
            password = forms.cleaned_data['password']
            print(email)
            print(password)
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)

                if user.is_superuser:
                    print('---------------------------------')
                    print('---------------------------------')
                    print('---------------------------------')
                return redirect('dashboard')
            else:
                messages.error(request, 'wrong username password')
    context = {'form': forms}
    return render(request, 'adminLogin.html', context)


# def resgister_page(request):

#     forms = registerForm()
#     if request.method == 'POST':
#         forms = registerForm(request.POST)
#         if forms.is_valid():
#             forms.save()
#             username = forms.cleaned_data['username']
#             password = forms.cleaned_data['password1']
#             user = authenticate(username=username, password=password)
#             if user:
                
#                 messages.error(request, 'user already exsist')
#                 return redirect('dashboard')
#             else:
#                 return redirect('resgister')
#         else:
#             print(forms.errors)
#     else:
#         print(forms.as_p)

#         context = {'form': forms}

#         return render(request, 'users/resgister.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')

def user_list(request):

    data = User.objects.all()

    return render(request, 'user_list.html', { 'data' : data})
