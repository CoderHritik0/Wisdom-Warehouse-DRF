from django.urls import path
from  . import views

urlpatterns = [
  path('notes/', views.NoteListCreateView.as_view(), name='note-list-create'),
  path('notes/hidden/', views.HiddenNoteListView.as_view(), name='hidden-note-list'),
  path('notes/delete/<int:pk>/', views.NoteDeleteView.as_view(), name='note-delete'),
  path('notes/update/<int:pk>/', views.NoteUpdateView.as_view(), name='note-update'),
  path('profile/', views.ProfileView.as_view(), name='profile-view'),
]