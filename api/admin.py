from django.contrib import admin
from .models import Note, Profile, NoteImage

class NoteAdmin(admin.ModelAdmin):
  list_display = ('id', 'title', 'user', 'is_hidden', 'created_at', 'updated_at')

class NoteImageAdmin(admin.ModelAdmin):
  list_display = ('id', 'note', 'image')

class ProfileAdmin(admin.ModelAdmin):
  list_display = ('id', 'user', 'avatar', 'pin')

# Register your models here.
admin.site.register(Note, NoteAdmin)
admin.site.register(NoteImage, NoteImageAdmin)
admin.site.register(Profile, ProfileAdmin)