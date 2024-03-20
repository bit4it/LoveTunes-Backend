from apps.music.models import ListeningSession
from apps.accounts.models import CustomUser
from tools.exceptions import CustomAPIException


class ListeningSessionManager:
    def create_session(self, creator: CustomUser) -> ListeningSession:
        try:
            session = ListeningSession.objects.get(creator=creator, is_active=True)        
        except:
            session = ListeningSession.objects.create(creator=creator)
            session.participants.add(creator)

        return session

    
    def end_session(self, session_id: str, creator: CustomUser) -> ListeningSession:
        session = self._get_active_listening_session(session_id=session_id)
        session.end_session()
        return session

    def join_session(self, session_id: str, user: CustomUser):
        session = self._get_active_listening_session(session_id=session_id)
        session.participants.add(user)
        return session
    
    def leave_session(self, session_id: str, user: CustomUser):
        session = self._get_active_listening_session(session_id=session_id)
        session.participants.remove(user)
        return session

    def _get_active_listening_session(self, session_id) -> ListeningSession:
        try:
            session = ListeningSession.objects.get(session_id=session_id, is_active=True)
            return session
                
        except:
            raise CustomAPIException(detail="Active Session Not Found")
