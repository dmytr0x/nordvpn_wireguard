# NordVPN + WireGuard configs generator

The script generates WireGuard configuration files using the infrastructure provided by NordVPN.

## Dependencies
```sh
go-task
python 3.13
```

## Installation
```sh
brew install go-task
uv python install
uv sync
```

## Activate venv
```sh
source .venv/bin/activate
```

## Run the script
```sh
task cli
```
