import uuid

class UniqueIdGenerator:
    @staticmethod
    def generate_listening_session_id():
        session_id = f"lis-{str(uuid.uuid4().hex)[:8]}-sess"
        return session_id
