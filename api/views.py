from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics

from api.models import Note
from .serializers import UserSerializer, NoteSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.
class UserCreateView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [AllowAny]

class NoteListCreateView(generics.ListCreateAPIView):
  serializer_class = NoteSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    queryset = Note.objects.filter(user=self.request.user, is_hidden=False)
    return queryset

  def perform_create(self, serializer):
      if serializer.is_valid():
        serializer.save(user=self.request.user)
      else:
        print(serializer.errors)

class HiddenNoteListView(generics.ListAPIView):
  serializer_class = NoteSerializer
  permission_classes = [IsAuthenticated]

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
      return self.request.user.userprofile
  
  def perform_update(self, serializer):
      serializer.save()