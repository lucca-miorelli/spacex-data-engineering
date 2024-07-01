from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field


class Failure(BaseModel):
    time: Optional[int]
    altitude: Optional[int]
    reason: Optional[str]


class Fairings(BaseModel):
    reused: Optional[bool]
    recovery_attempt: Optional[bool]
    recovered: Optional[bool]
    ships: Optional[List[str]]


class CrewRole(BaseModel):
    crew: Optional[str]
    role: Optional[str]


class Core(BaseModel):
    core: Optional[str]
    flight: Optional[int]
    gridfins: Optional[bool]
    legs: Optional[bool]
    reused: Optional[bool]
    landing_attempt: Optional[bool]
    landing_success: Optional[bool]
    landing_type: Optional[str]
    landpad: Optional[str]


class Patch(BaseModel):
    small: Optional[str]
    large: Optional[str]


class Reddit(BaseModel):
    campaign: Optional[str]
    launch: Optional[str]
    media: Optional[str]
    recovery: Optional[str]


class Flickr(BaseModel):
    small: List[str]
    original: List[str]


class Links(BaseModel):
    patch: Patch
    reddit: Reddit
    flickr: Flickr
    presskit: Optional[str]
    webcast: Optional[str]
    youtube_id: Optional[str]
    article: Optional[str]
    wikipedia: Optional[str]


class Launch(BaseModel):
    flight_number: int = Field(...)
    name: str = Field(..., unique=True)
    date_utc: str = Field(...)
    date_unix: int = Field(...)
    date_local: str = Field(...)
    date_precision: str = Literal["hour", "day", "month"]
    static_fire_date_utc: Optional[str]
    static_fire_date_unix: Optional[int]
    tbd: bool = False
    net: bool = False
    window: Optional[int]
    rocket: Optional[str]
    success: Optional[bool]
    failures: List[Failure]
    upcoming: bool = Field(...)
    details: Optional[str]
    fairings: Optional[Fairings]
    crew: List[Union[CrewRole, str]]
    ships: List[str]
    capsules: List[str]
    payloads: List[str]
    launchpad: Optional[str]
    cores: List[Core]
    links: Links
    auto_update: bool = True
    launch_library_id: Optional[str]
    id: str = Field(..., unique=True)
