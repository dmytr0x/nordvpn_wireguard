import base64

from http import HTTPStatus
from typing import Any, Literal, TypedDict

import httpx

from src.btypes import Item, NameValue

WireguardProtocol = Literal["wireguard_udp"]


class Credentials(TypedDict):
    id: int
    private_key: str
    password: str
    username: str


class Country(TypedDict):
    id: int
    name: str
    serverCount: int
    code: str


class City(TypedDict):
    name: str


class LocationCountry(TypedDict):
    name: str
    city: City


class Location(TypedDict):
    id: int
    country: LocationCountry


class Technology(TypedDict):
    identifier: WireguardProtocol
    metadata: list[NameValue]


class Server(TypedDict):
    id: int
    name: str
    locations: list[Location]
    station: str
    technologies: list[Technology]


def fetch_credentials(token: str) -> Credentials | None:
    token_encoded = base64.b64encode(f"token:{token}".encode())
    headers = {"Authorization": f"Basic {token_encoded.decode()}"}

    url = "https://api.nordvpn.com/v1/users/services/credentials"
    resp = httpx.get(url, headers=headers)
    if resp.status_code != HTTPStatus.OK:
        return None

    data = resp.json()
    return {
        "id": data["id"],
        "private_key": data["nordlynx_private_key"],
        "password": data["password"],
        "username": data["username"],
    }


def _get(url: str) -> Any:  # noqa: ANN401
    resp = httpx.get(url)
    if resp.status_code != HTTPStatus.OK:
        return None

    return resp.json()


def fetch_countries() -> list[Item[Country]] | None:
    countries: list[Country] | None = _get("https://api.nordvpn.com/v1/servers/countries")
    if not countries:
        return None

    return [
        {
            "title": "{name} ({serverCount})".format(
                name=country["name"],
                serverCount=country["serverCount"],
            ),
            "data": country,
        }
        for country in countries
    ]


def fetch_recommendations(
    country_id: int,
    limit: int = 250,
) -> list[Item[Server]] | None:
    url = (
        "https://api.nordvpn.com/v1/servers/recommendations"
        "?filters[servers_technologies][identifier]=wireguard_udp"
        f"&limit={limit}"
        f"&filters[country_id]={country_id}"
    )
    servers: list[Server] | None = _get(url)
    if not servers:
        return None

    return [
        {
            "title": "{name} ({city})".format(
                name=server["name"],
                city=server["locations"][0]["country"]["city"]["name"],
            ),
            "data": server,
        }
        for server in servers
    ]


def render_config_template(
    credentials: Credentials,
    server: Server,
    address: str = "10.5.0.2/32",
    dns: str = "9.9.9.9, 1.1.1.1",
    allowed_ips: str = "0.0.0.0/0",
) -> str:
    wireguards = (s for s in server["technologies"] if s["identifier"] == "wireguard_udp")
    wireguard = next(wireguards)
    public_key = wireguard["metadata"][0]["value"]

    return f"""
    [Interface]
    Address = {address}
    PrivateKey = {credentials["private_key"]}
    DNS = {dns}

    [Peer]
    PublicKey = {public_key}
    Endpoint = {server["station"]}:51820
    AllowedIPs = {allowed_ips}
    """
