from django.contrib import admin
from .models import Note, Profile

class NoteAdmin(admin.ModelAdmin):
  list_display = ('id', 'title', 'user', 'is_hidden', 'created_at', 'updated_at')

# Register your models here.
admin.site.register(Note, NoteAdmin)
# admin.site.register(NoteImage)
admin.site.register(Profile)