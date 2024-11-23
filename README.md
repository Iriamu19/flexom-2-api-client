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

1. Clone the repository:
   ```bash
   git clone https://github.com/Iriamu19/flexom-hemis-api-client
   cd flexom-api-client
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   ```bash
   cp .env.example .env
   ```
   Update the `.env` file with your Ubiant credentials:
   ```
   EMAIL=your-ubiant-email
   PASSWORD=your-ubiant-password
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
