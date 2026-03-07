# Digital Loggers – ASCOM Alpaca Server for Digital Loggers ePDUs

A FastAPI-based server, implementing the ASCOM **ISwitchV3** interface.  Communication is via REST to the onboard
TCP server of the ePDU. Uses the dlipower library.

---

## Implemented ISwitchV3 capabilities as of this driver version

| Property/Method      | Supported |
|----------------------|-----------|
| MaxSwitch            | ✔         |
| CanAsync             | ✘         |
| CanWrite             | ✔         |
| GetSwitch            | ✔         |
| GetSwitchDescription | ✘         |
| GetSwitchName        | ✔         |
| GetSwitchValue       | ✔         |
| MinSwitchValue       | ✔         |
| MaxSwitchValue       | ✔         |
| SetAsync             | ✘         |
| SetAsyncValue        | ✘         |
| SetSwitch            | ✔         |
| SetSwitchName        | ✘         |
| SetSwitchValue       | ✔         |
| StateChangeComplete  | ✘         |
| SwitchStep           | ✔         |

Tested on the Digital Loggers EPC7.

---

## Architecture

| File               | Purpose                                     |
|--------------------|---------------------------------------------|
| `main.py`          | FastAPI app, lifespan, router wiring        |
| `config.py`        | Pydantic config models, YAML loader         |
| `config.yaml`      | User-editable configuration                 |
| `switch.py`        | FastAPI router – ISwitchV3 endpoints        |
| `switch_device.py` | Low-level driver                            |
| `management.py`    | `/management` Alpaca management endpoints   |
| `setup.py`         | `/setup` HTML stub pages                    |
| `discovery.py`     | UDP Alpaca discovery responder (port 32227) |
| `responses.py`     | Pydantic response models                    |
| `exceptions.py`    | ASCOM Alpaca error classes                  |
| `shr.py`           | Shared FastAPI dependencies / helpers       |
| `log.py`           | Loguru config + stdlib intercept handler    |
| `test.py`          | Quick smoke-test script                     |
| `requirements.txt` | Python package dependencies                 |
| `Dockerfile`       | Container build                             |

---

## Configuration

Edit `config.yaml` to match your dome setup.

Currently assumes that the user defines names that match those set via the DLI web API.

Multiple Digital Loggers switches can be registered by adding further entries under
`devices:` with distinct `device_number` values.


---

## Quick start

```bash
pip install -r requirements.txt
python main.py
```

The server starts on `0.0.0.0:6000` by default (configurable in `config.yaml`).

---

## Smoke test

```bash
# Requires hardware connected, i.e. will move dome
python test.py
```

---

## Docker

```bash
docker build -t alpaca-digital-loggers .
docker run -d --name alpaca-digital-loggers \
    --network host \
    --env-file .env \
    --restart unless-stopped \
    alpaca-digital-loggers
docker logs -f alpaca-digital-loggers
```