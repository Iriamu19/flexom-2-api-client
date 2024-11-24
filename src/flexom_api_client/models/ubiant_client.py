import json
import os
from pathlib import Path
import tempfile

import requests
from dotenv import load_dotenv

from ..logger_config import logger

load_dotenv()


class ERROR_401(Exception):
    pass


class UbiantClient:
    """A singleton low level API client"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        logger.debug("Creating UbiantClient instance.")
        self.request_session = requests.session()
        self.base_url = "https://hemisphere.ubiant.com"
        infos = self._get_cached_or_new_connection_infos()
        self.token = infos["token"]
        self.building_id = infos["building_id"]
        self.hemis_base_url = infos["hemis_base_url"]

    def _make_hemis_request(
        self, method: str, url: str, data=None, params=None
    ) -> dict:
        """
        Centralized method for making authenticated API requests.

        Will try to actualize the token if the first request
        get an authentication error 401.

        :param method: HTTP method ("GET", "POST", etc.)
        :param url: URL for the request.
        :param data: Optional payload for POST requests.
        :param params: Optional query parameters.
        :return: Parsed JSON response or raises an error.
        """
        for _ in range(2):
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Building-Id": self.building_id,
            }
            req_url = self.hemis_base_url + url
            try:
                r = self._make_request(
                    method=method,
                    url=req_url,
                    headers=headers,
                    data=data,
                    params=params,
                )
                return r
            except ERROR_401:
                self.token = self._get_cached_or_new_connection_infos(force_new=True)[
                    "token"
                ]

    def _make_request(
        self, method: str, url: str, headers=None, data=None, params=None
    ):
        """
        Centralized method for making API requests.

        :param method: HTTP method ("GET", "POST", etc.)
        :param url: URL for the request.
        :param headers: Optional request headers.
        :param data: Optional payload for POST requests.
        :param params: Optional query parameters.
        :return: Parsed JSON response or raises an error.
        """
        try:
            logger.debug(f"{method} {url}")
            response = self.request_session.request(
                method=method,
                url=url,
                headers=headers,
                json=data,  # Using JSON format for data
                params=params,
            )
            response.raise_for_status()
            if len(response.content) > 0:
                return response.json()
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            if str(response.status_code) == "401":
                raise ERROR_401
        except requests.exceptions.RequestException as req_err:
            logger.error(f"Error occurred during the request: {req_err}")
        return None

    def _get_cached_or_new_connection_infos(self, force_new=False) -> dict | None:
        """Get cached connecton infos from a file or fetch a new one."""
        cache_file_path = Path(tempfile.gettempdir()).joinpath("cached_flexom_connection.json")
        if cache_file_path.exists():
            cache_file_path.chmod(0o600)
        if not force_new:
            cached_infos = None
            if Path(cache_file_path).exists():
                with open(cache_file_path, 'r') as file:
                    cached_infos = json.load(file)
                expected_keys = {"token", "building_id", "hemis_base_url"}
                all_keys_present = expected_keys.issubset(cached_infos.keys())
                if all_keys_present:
                    return cached_infos
            else:
                logger.debug("No cached file.")

        logger.debug("Retrieving connection infos.")
        new_infos = {}
        new_token = self._fetch_token()
        new_infos["token"] = new_token
        self.token = new_token
        infos = self.get_my_infos()
        new_infos["building_id"] = infos[0]["buildingId"]
        new_infos["hemis_base_url"] = infos[0]["hemis_base_url"]
        with open(cache_file_path, "w") as file:
            json.dump(new_infos, file, indent=4)
        logger.debug("New token retrieved.")
        return new_infos

    def _fetch_token(self) -> str | None:
        """Fetch the token by logging in with email and password."""
        body = {
            "email": os.getenv("EMAIL"),
            "password": os.getenv("PASSWORD"),
        }
        url = f"{self.base_url}/users/signin"
        response = self._make_request("POST", url, data=body)
        if response is None:
            logger.error("Failed to retrieve new token.")
            return None
        token = response.get("token")
        return token

    def get_my_infos(self):
        """Fetch user's building information."""
        headers = {"Authorization": f"Bearer {self.token}"}
        url = f"{self.base_url}/buildings/mine/infos"
        return self._make_request("GET", url, headers=headers)

    def get_sensors(self):
        """Fetch sensor data for the building."""
        url = "/intelligent-things/sensors"
        return self._make_hemis_request("GET", url)

    def get_actuators(self):
        """Fetch actuator data for the building."""
        url = "/intelligent-things/actuators"
        return self._make_hemis_request("GET", url)

    def set_actuator_value(self, it_id, actuator_id, value):
        url = f"/intelligent-things/{it_id}/actuator/{actuator_id}/state"
        body = {"value": value}
        return self._make_hemis_request("PUT", url, data=body)

    def get_all_intelligent_things(self):
        url = "/intelligent-things/listV2"
        return self._make_hemis_request("GET", url)

    def set_multiple_actuators_value(self, it_id, actuator_id, value):
        url = "/intelligent-things/actuators/state"
        body = {
            "pref": {
                "value": value,
                "duration": 0,
            },
            "actuators": [{"itId": it_id, "actuatorIds": [actuator_id]}],
        }
        self._make_hemis_request("PUT", url, body)

    def get_all_zones(self):
        url = "/zones"
        return self._make_hemis_request("GET", url)

    def get_all_zone_names(self):
        zones = self.get_all_zones()
        return [zone.get("name") for zone in zones]
