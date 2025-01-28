# ruff: noqa: ANN001, ANN101, ANN201, S101, PLR2004
import pytest

from src.nordvpn import render_config_template


@pytest.fixture
def mock_credentials():
    return {"private_key": "mock_private_key"}


@pytest.fixture
def mock_server():
    return {
        "station": "128.128.128.128",
        "technologies": [
            {
                "identifier": "wireguard_udp",
                "metadata": [{"value": "mock_public_key"}],
            }
        ],
    }


def test_render_config_template_defaults(mock_credentials, mock_server):
    expected_output = """[Interface]
Address = 10.5.0.2/32
PrivateKey = mock_private_key
DNS = 9.9.9.9, 1.1.1.1

[Peer]
PublicKey = mock_public_key
Endpoint = 128.128.128.128:51820
AllowedIPs = 0.0.0.0/0
"""
    result = render_config_template(mock_credentials, mock_server)
    assert result == expected_output


def test_render_config_template_custom_values(mock_credentials, mock_server):
    address = "192.168.1.2/24"
    dns = "8.8.8.8, 8.8.4.4"
    allowed_ips = "192.168.1.0/24"

    expected_output = f"""[Interface]
Address = {address}
PrivateKey = mock_private_key
DNS = {dns}

[Peer]
PublicKey = mock_public_key
Endpoint = 128.128.128.128:51820
AllowedIPs = {allowed_ips}
"""
    result = render_config_template(
        mock_credentials,
        mock_server,
        address=address,
        dns=dns,
        allowed_ips=allowed_ips,
    )
    assert result == expected_output


def test_render_config_template_missing_wireguard(mock_credentials):
    mock_server = {
        "station": "mock.server.com",
        "technologies": [{"identifier": "some_other_tech"}],
    }

    with pytest.raises(StopIteration):  # This will occur if `next` has no elements
        render_config_template(mock_credentials, mock_server)


def test_render_config_template_missing_metadata(mock_credentials):
    mock_server = {
        "station": "mock.server.com",
        "technologies": [
            {
                "identifier": "wireguard_udp",
                "metadata": [],
            }
        ],
    }

    with pytest.raises(IndexError):  # This will occur if `metadata` is empty
        render_config_template(mock_credentials, mock_server)


def test_render_config_template_invalid_credentials(mock_server):
    mock_credentials = {"wrong_key": "mock_private_key"}

    with pytest.raises(KeyError):
        render_config_template(mock_credentials, mock_server)
