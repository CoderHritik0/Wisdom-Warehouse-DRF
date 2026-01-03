from django.contrib.auth.models import User
from .models import Note, Profile, NoteImage
from rest_framework import serializers

class NoteImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = NoteImage
    fields = ['id', 'image']
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
    extra_kwargs = {'password': {'write_only': True}}

  def create(self, validated_data):
    user = User.objects.create_user(**validated_data)
    return user
    
  def update(self, instance, validated_data):
    proceed_with_update = True
    old_password = self.context['request'].data.get('old_password')
    new_password = self.context['request'].data.get('new_password')
    if new_password:
      proceed_with_update = False
      if old_password is None:
        raise serializers.ValidationError({"password": "Current password is required to set a new password."})
      if not instance.check_password(old_password):
        raise serializers.ValidationError({"password": "Current password is incorrect."})
      instance.set_password(new_password)
      proceed_with_update = True
    if proceed_with_update:
      for attr, value in validated_data.items():
        setattr(instance, attr, value)

    instance.save()
    return instance

class NoteSerializer(serializers.ModelSerializer):
  images = NoteImageSerializer(many=True, read_only=True)
  class Meta:
    model = Note
    fields = '__all__'
    extra_kwargs = {
      'user': {'read_only': True},
      'created_at': {'read_only': True},
      'updated_at': {'read_only': True},
    }

  def create(self, validated_data):
    request = self.context['request']
    images_data = request.FILES.getlist('images')
    note = Note.objects.create(**validated_data)
    for image_data in images_data:
      NoteImage.objects.create(note=note, image=image_data)
    return note
  
  def update(self, instance, validated_data):
    request = self.context['request']
    images_data = request.FILES.getlist('images')
    note = super().update(instance, validated_data)
    for image_data in images_data:
      NoteImage.objects.create(note=note, image=image_data)
    return note

class ProfileSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  class Meta:
    model = Profile
    fields = ['avatar', 'pin', 'user']
    
class ResetPasswordEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(required=True)
  
class ResetPasswordSerializer(serializers.Serializer):
  new_password = serializers.CharField(
      min_length=8,
      max_length=128,
      write_only=True,
      error_messages={'invalid': 'Password must be at least 8 characters long.'}
  )
  confirm_password = serializers.CharField(write_only=True)

  def validate(self, attrs):
      if attrs['new_password'] != attrs['confirm_password']:
          raise serializers.ValidationError("Passwords do not match.")
      return attrs