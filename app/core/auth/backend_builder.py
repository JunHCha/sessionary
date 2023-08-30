import uuid

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, CookieTransport
from httpx_oauth.clients.google import GoogleOAuth2

from app.core.auth.manager import UserManager
from app.core.settings.base import AppSettings
from app.db.tables import User
from app.depends.auth import get_database_strategy, get_user_manager
from app.depends.config import get_app_settings

settings = get_app_settings()


class AuthBackendBuilder:
    def __init__(self, settings: AppSettings, user_manager: UserManager) -> None:
        self._user_manager = user_manager
        self._cookie_name = settings.cookie_name
        self._cookie_max_age = settings.auth_session_expire_seconds
        self._google_client_id = settings.google_client_id
        self._google_client_secret = settings.google_client_secret

    def get_fastapi_users(self) -> FastAPIUsers:
        auth_backend = self._get_auth_backend()
        return FastAPIUsers[User, uuid.UUID](self._user_manager, [auth_backend])

    def get_oauth2_client(self) -> GoogleOAuth2:
        oauth2_client = GoogleOAuth2(
            client_id=self._google_client_id,
            client_secret=self._google_client_secret,
        )

        return oauth2_client

    def _get_auth_backend(self) -> AuthenticationBackend:
        cookie_transport = CookieTransport(
            cookie_name=self._cookie_name, cookie_max_age=self._cookie_max_age
        )

        auth_backend = AuthenticationBackend(
            name="database",
            transport=cookie_transport,
            get_strategy=get_database_strategy,
        )

        return auth_backend


cookie_transport = CookieTransport(
    cookie_name=settings.cookie_name,
    cookie_max_age=settings.auth_session_expire_seconds,
)

auth_backend = AuthenticationBackend(
    name="database",
    transport=cookie_transport,
    get_strategy=get_database_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user()

google_oauth_client = GoogleOAuth2(
    settings.google_client_id, settings.google_client_secret
)
