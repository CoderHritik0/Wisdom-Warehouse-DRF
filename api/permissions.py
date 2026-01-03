from rest_framework.permissions import BasePermission

class PinVerifiedPermission(BasePermission):
  """
  Custom permission to only allow access to hidden notes if the correct PIN is provided.
  """

  message = 'Incorrect PIN.'
  
  def has_permission(self, request, view):
    pin = request.data.get('pin')
    if pin and request.user.profile.pin == pin:
      return True
    return False