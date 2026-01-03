from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from Wisdom_Warehouse_DRF import settings

from api.filters import NoteOwnerFilter
from api.models import Note, NoteImage, Profile
from .serializers import (UserSerializer,
                          NoteSerializer,
                          ProfileSerializer,
                          NoteImageSerializer,
                          ResetPasswordEmailSerializer,
                          ResetPasswordSerializer)
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import PinVerifiedPermission
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from django.core.mail import send_mail


# Create your views here.
class UserCreateView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [AllowAny]

class UserUpdateView(generics.UpdateAPIView):
  serializer_class = UserSerializer
  permission_classes = [IsAuthenticated]

  def get_object(self):
    return get_object_or_404(User, id=self.request.user.id)

  def perform_update(self, serializer):
    serializer.save()

class NoteListCreateView(generics.ListCreateAPIView):
  serializer_class = NoteSerializer
  permission_classes = [IsAuthenticated]
  filter_backends = [NoteOwnerFilter]

  def get_queryset(self):
    queryset = Note.objects.prefetch_related('images').filter(is_hidden=False)
    return queryset

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

class HiddenNoteListView(generics.ListAPIView):
  serializer_class = NoteSerializer
  permission_classes = [IsAuthenticated, PinVerifiedPermission]
  pagination_class = None

  def get_queryset(self):
    return Note.objects.filter(user=self.request.user, is_hidden=True)

class NoteUpdateView(generics.UpdateAPIView):
  serializer_class = NoteSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    return Note.objects.filter(user=self.request.user)
  
  def perform_update(self, serializer):
    serializer.save()

class NoteDeleteView(generics.DestroyAPIView):
  serializer_class = NoteSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    return Note.objects.filter(user=self.request.user)

class ProfileView(generics.RetrieveUpdateAPIView):
  serializer_class = ProfileSerializer
  permission_classes = [IsAuthenticated]

  def get_object(self):
    return self.request.user.profile
  
  def perform_update(self, serializer):
    profile = Profile.objects.get(user=self.request.user)
    if profile.avatar and 'avatar' in self.request.FILES:
      profile.avatar.delete(save=False)
    serializer.save()
    profile = serializer.instance

class NoteImageDeleteView(generics.DestroyAPIView):
  serializer_class = NoteImageSerializer
  permission_classes = [IsAuthenticated]

  def delete(self, request, **kwargs):
    note_id = self.kwargs['pk']
    image_id = self.kwargs['image_id']
    try:
      note_image = NoteImage.objects.get(id=image_id, note__id=note_id, note__user=request.user)
      note_image.image.delete(save=False)
      note_image.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
    except NoteImage.DoesNotExist:
      return Response({"message": "Note image not found.", "success": False}, status=status.HTTP_404_NOT_FOUND)
    
class RequestPasswordReset(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordEmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.filter(email__iexact=email).first()

        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"{settings.PASSWORD_RESET_BASE_URL}/{uid}/{token}"

            # Send email with reset link
            send_mail(
                subject="Password Reset Request",
                message=f"Click the link to reset your password: {reset_url}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            return Response({'detail': 'Password reset link sent.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User with this email not found.'}, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordConfirmView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model()._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and PasswordResetTokenGenerator().check_token(user, token):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'detail': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)