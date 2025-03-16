from django.shortcuts import get_object_or_404
from authen_app.serializer import UserSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
# Create your views here.

class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = User.objects.get(username=serializer.data['username'],
                                            email=serializer.data['email'],)
            token = Token.objects.create(user=user)
            user.set_password(request.data['password'])
            user.save()

            return Response({"user": serializer.data, "token": token.key})
        return Response(serializer.errors)

class UserViewLogin(APIView):
        def post(request, self):
             pass