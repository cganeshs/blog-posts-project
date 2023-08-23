from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics
from .serializers import LoginSerializer, RegisterSerializer
from rest_framework.authtoken.models import Token

# View for user login
class UserLoginView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    def create(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                # Create or retrieve a token for the user
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            return Response({'message': 'Login failed'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# View for user registration
class UserRegistration(generics.CreateAPIView):
    # Allow any user to access this view
    permission_classes = [AllowAny]
    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutView(generics.ListAPIView):
    def list(self,request):
        if request.method == 'GET':
            request.user.auth_token.delete()
            return Response({'message':'Successfully logout'})