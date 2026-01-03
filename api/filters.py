import django_filters
from api.models import Note
from rest_framework import filters

class NoteOwnerFilter(filters.BaseFilterBackend):
  """
  Filter that ensures users can only access their own notes.
  """

  def filter_queryset(self, request, queryset, view):
    return queryset.filter(user=request.user)