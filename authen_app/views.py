from django.shortcuts import get_object_or_404
from authen_app.serializer import UserSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
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
        def post(self, request):
             username = request.data.get('username')
             password = request.data.get('password')
             password_match = request.data.get('password_match')

             if password != password_match:
                  return Response({"detail": "Passwords aren't match!"})
             
             if not username or not password:
                  return Response({"detail": "Username don't exist or password is incorrect"})
                             
             user = authenticate(username=username, password=password)
             user_data = UserSerializer(user).data
             if user:
                  token, created = Token.objects.get_or_create(user=user)
                  return Response({'token': token.key,
                                   "user": user_data})
             
             else:
                  return Response({'detail': "User doesn't exist"})
             
                          # {"username": "exile", "password": "123!", "password_match": "123!"}


class UserViewLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
         request.user.auth_token.delete() # return errror but maybe I just post wrong data dsdsd

         return Response({'message': 'Successfully logout'})
          