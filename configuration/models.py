from dataclasses import dataclass


@dataclass
class JwtParams:
    algorithm: str
    expiration: int


@dataclass
class SettingsYml:
    jwt: JwtParams
