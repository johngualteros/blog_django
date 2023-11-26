from django.shortcuts import render

# Create your views here.
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import (api_settings)
from rest_framework.views import APIView
from user.serializers import UserSerializer, AuthTokenSerializer
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework import status


class SendEmailView(APIView):
    def post(self, request, *args, **kwargs):
        subject = request.data.get('subject', '')
        message = request.data.get('message', '')
        from_email = 'tu-correo@example.com'
        recipient_list = [request.data.get('recipient', '')]

        try:
            send_mail(subject, message, from_email, recipient_list)
            return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        # Llama al método perform_create en la superclase
        user = serializer.save()

        # Envía un correo electrónico después de crear el usuario
        subject = 'Bienvenido a nuestra plataforma'
        message = f'Hola {user.name},\n\n¡Gracias por registrarte en nuestra plataforma!'
        from_email = 'noreply@example.com'
        recipient_list = [user.email]

        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            # Maneja el error si el envío de correo electrónico falla
            print(f'Error sending email: {e}')


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user
