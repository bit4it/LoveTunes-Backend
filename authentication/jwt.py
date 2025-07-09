from rest_framework_simplejwt.tokens import RefreshToken

class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        
        # Add custom claims
        token['user_uid'] = user.uid
        token['email'] = user.email
        token['first_name'] = user.first_name or ''
        token['last_name'] = user.last_name or ''
        token['is_premium'] = user.is_premium
        token['status'] = user.status
        token['is_email_verified'] = user.is_email_verified
        token['full_name'] = f"{user.first_name or ''} {user.last_name or ''}".strip()
        
        # Add timestamp info
        token['created_on'] = user.created_on.isoformat() if user.created_on else None
        token['updated_on'] = user.updated_on.isoformat() if user.updated_on else None
        
        return token