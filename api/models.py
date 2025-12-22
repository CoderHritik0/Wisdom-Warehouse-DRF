from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# import markdown
# import bleach
# from django.utils.safestring import mark_safe

# Create your models here.
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    tag = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=6, default="ffffff")
    is_hidden = models.BooleanField(default=False)
    # is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def formatted_description(self):
    #     html = markdown.markdown(self.description, extensions=['fenced_code', 'tables'])
    #     clean_html = bleach.clean(html, tags=['p','pre','code','strong','em','ul','ol','li','a','h1','h2','h3','blockquote'])
    #     return mark_safe(clean_html)

    def __str__(self):
        return f'{self.user.username} - {self.note_id}';

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    avatar = models.ImageField(upload_to='profiles/', blank=True, null=True)
    pin = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


# 🔹 Auto-create or update Profile whenever a User is created
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

# class NoteImage(models.Model):
#     id = models.AutoField(primary_key=True)
#     note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='images')
#     image = models.ImageField(upload_to='note_images/')

#     def __str__(self):
#         return f'Image {self.id} for Note {self.note.note_id}'