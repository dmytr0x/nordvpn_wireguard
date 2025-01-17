import pathlib

from src import core, nordvpn, ui


def main() -> None:
    token = input("Enter the NordVPN Access Token: ")
    token = token.strip()
    if not token:
        core.terminate("No acceess token is provided")

    credentials = nordvpn.fetch_credentials(token)
    if not credentials:
        core.terminate("Cannot fetch the NordVPN credentials")

    country = None
    if countries := nordvpn.fetch_countries():
        country = ui.select_single_item(countries)
    if not country:
        core.terminate("Cannot find any countries")

    selected_servers = None
    if servers := nordvpn.fetch_recommendations(country["id"]):
        selected_servers = ui.select_multiple_items(servers)
    if not selected_servers:
        core.terminate("Cannot find any recommended servers")

    for server in selected_servers:
        config = nordvpn.render_config_template(
            credentials=credentials,
            server=server,
        )

        server_name = (
            f"{server['name']}_{server['locations'][0]['country']['city']['name']}".lower()
            .replace("#", "")
            .replace(" ", "_")
        )
        config_filename = f"{server_name}.conf"
        with pathlib.Path(config_filename).open("w") as f:
            _ = f.write(config)

        print(f"New configuration has been created: {config_filename}")  # noqa: T201


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        core.terminate("The script has been stopped")
