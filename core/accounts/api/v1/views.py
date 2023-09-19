from rest_framework import generics
from rest_framework.response import Response
from .serializers import (RegistrationSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainpairSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    ActivationResendApiSerializer)
from rest_framework.authtoken.views import ObtainAuthToken  
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly 
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.models import User
from ...models import Profile
from django.shortcuts import get_object_or_404
from mail_templated import send_mail, EmailMessage
from ..utils import EmailThread
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings



class RegistrationApiView(generics.GenericAPIView):
    """
    registration user 
    """
    # permission_classes = [IsAuthenticated]
    serializer_class = RegistrationSerializer
    # queryset = Post.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data['email']
            data={
                'email': email
            }
            user_obj = get_object_or_404(User, email = email)
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage('email/activation_email.tpl', {'token':token}, 'iman.najjari9494@gmail.com', to=[email])
            EmailThread(email_obj).start()
            return Response(data, status=201)
        return Response(serializer.errors,  status=400)
    
        
        

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class CustomDiscardAuthToekn(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=204)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainpairSerializer

class ChangePasswordApiView(generics.GenericAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    
    def put(self, request=None):
        self.object = self.get_object()
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password":["wrong password."]}, status = 400)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"detail":"password Change successfully"}, status=200)
        # return super().update(request, *args, **kwargs)
        return Response(serializer.errors, status=400)

class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj

class TestEmailSend(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        self.email = 'iman.najjari9494@gmail.com'
        user_obj = get_object_or_404(User, email = self.email)
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage('email/hello.tpl', {'token':token}, 'iman.najjari9494@gmail.com', to=[self.email])
        EmailThread(email_obj).start()

        return Response("email send")

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ActivationApiView(APIView):
    def get(self, request, token,*args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")
        except:
            return Response({"detail":"token has been expired"}, status=400)
        user_obj = User.object.get(pk = user_id)
        if user_obj.is_verified:
            return Response({"detail":"your account have been verified "})
        user_obj.is_verified = True
        user_obj.save()
        return Response({"detail":"your account have been verified and activated successfully"})


class ActivationResendApiView(generics.GenericAPIView):
    serializer_class = ActivationResendApiSerializer
    def post(self, request,*args, **kwargs):
        serializer = ActivationResendApiSerializer(data = request.data)
        if serializer.is_valid():
            user_obj = serializer.validated_data['user']
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage('email/activation_email.tpl', {'token':token}, 'iman.najjari9494@gmail.com', to=[user_obj.email])
            EmailThread(email_obj).start()
            return Response({"detail":"user activation resend successfully"}, status=200)
        else:
            return Response({"detail":"invalid request"}, status=400)
    
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

