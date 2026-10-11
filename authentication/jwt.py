from typing import Optional

from rest_framework_simplejwt.authentication import AuthUser, JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, Token
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

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



class CustomJwtAuthentication(JWTAuthentication):

    def authentication_ws_request(self, headers):
        """
        Extract JWT from WebSocket headers, validate it,
        and return the authenticated user.
        """
        headers_dict = {
            key.decode("latin1").lower(): value.decode("latin1")
            for key, value in headers
        }

        auth_header = headers_dict.get("authorization")

        if not auth_header:
            raise AuthenticationFailed("Authorization header is missing")
        # Parse: Bearer <token>
        raw_token = self.get_raw_token(
            auth_header.encode("latin1")
        )

        if raw_token is None:
            raise AuthenticationFailed("Invalid authorization header")

        # Validate JWT signature, expiry, and token claims.
        validated_token = self.get_validated_token(raw_token)

        # Fetch the user associated with the validated token.
        user = self.get_user(validated_token)

        if not user:
            raise AuthenticationFailed("valid token not found...")

        return user

    def authenticate(self, request) -> Optional[tuple[AuthUser, Token]]:
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return AuthenticationFailed("Access token not found.")

        validated_token = self.get_validated_token(raw_token)

        user = self.get_user(validated_token)
        if not user:
            raise AuthenticationFailed("user not found.")

        return user, validated_token