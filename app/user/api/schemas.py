from pydantic import BaseModel

from app.models import UserArtistInfo


class GetArtistsResponse(BaseModel):
    data: list[UserArtistInfo]
