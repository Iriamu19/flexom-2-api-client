# Flexom Python API Client

## Overview

This project provides a Python client library for interacting with the **Flexom 2.0 Domotic Service**. It enables developers to programmatically control and retrieve data from a Ubiant-powered smart home system. The library simplifies interaction with actuators, sensors, and intelligent things, offering a high-level API for various operations.

---

## Features

- **Authentication and Session Management**
  - Automatically handles token-based authentication with caching.
- **Actuator Management**
  - Retrieve and modify the state of actuators.
- **Intelligent Thing Management**
  - Fetch intelligent devices with associated actuators and zones.
- **Sensor Integration**
  - Fetch and interact with sensor data.
- **CLI Tool**
  - Visualize smart home hierarchy in a tree view.
  - Update actuator values directly from the command line.

---

## Installation

1. Install the application :

- with pipx:

```
pipx install git+https://github.com/Iriamu19/flexom-2-api-client
```

- with uv:

```
uv tool install git+https://github.com/Iriamu19/flexom-2-api-client
```

2. Set up your config file:

Create a file in `$HOME/.config/flexom-api-client/config.json` with the following content:

```json
{
  "EMAIL": "your-ubiant-email",
  "PASSWORD": "your-ubiant-password"
}
```

---

## Usage

### Command Line Interface (CLI)

The library includes a CLI for quick interactions:

#### Display Actuators in a Tree View
```bash
python -m flexom_api_client actuators_tree_view
```

#### Set Actuator Value
```bash
python -m flexom_api_client set_actuator_value <actuator_id> <value> [--it_id <it_id>]
```

Example:
```bash
python -m flexom_api_client set_actuator_value actuator123 75 --it_id intelligentThing456
```
