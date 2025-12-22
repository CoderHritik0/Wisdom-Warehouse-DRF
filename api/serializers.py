from django.contrib.auth.models import User
from .models import Note, Profile
from rest_framework import serializers

# class NoteImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = NoteImage
#         fields = ['note', 'id', 'image']
#         extra_kwargs = {'note': {'read_only': True}, 'id': {'read_only': True}}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class NoteSerializer(serializers.ModelSerializer):
    # images = NoteImageSerializer(many=True)
    class Meta:
        model = Note
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}, 'created_at': {'read_only': True}, 'updated_at': {'read_only': True}, 'note_id': {'read_only': True}, 'is_deleted': {'read_only': True}}

    # def create(self, validated_data):
    #     images_data = validated_data.pop('images', [])
    #     print(images_data)
    #     note = Note.objects.create(**validated_data)
    #     for image_data in images_data:
    #         NoteImage.objects.create(note=note, **image_data)
    #     return note

class ProfileSerializer(serializers.ModelSerializer):
    userProfile = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = ['avatar', 'pin', 'userProfile']
        extra_kwargs = {'user': {'read_only': True}}