import os

import requests
import urllib3
import yaml
from models import CreateLabResponse

urllib3.disable_warnings()


class CML:
    def __init__(self) -> None:
        # Default url for CML from Devnet Sandbox.
        self._username = os.getenv("CML_USERNAME", "developer")
        self._password = os.getenv("CML_PASSWORD", "C1sco12345")
        self._url = os.getenv("CML_URL", "https://10.10.20.161")

        # Authentication token for CML.
        self._cml_token = self._authenticate().json()

    def _request(self, method: str, uri: str, **kwargs) -> requests.Response:
        if uri == "authenticate":
            headers = {"Content-Type": "application/json"}
        else:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._cml_token}",
            }

        response = requests.request(
            method=method,
            url=f"{self._url}/api/v0/{uri}",
            headers=headers,
            verify=False,
            **kwargs,
        )
        response.raise_for_status()
        return response

    def _authenticate(self) -> requests.Response:
        return self._request(
            "POST",
            "authenticate",
            json={"username": self._username, "password": self._password},
        )

    def _start_lab(self, lab_id: str) -> requests.Response:
        return self._request("PUT", f"labs/{lab_id}/start")

    def _load_cml_topology(self, payload: dict) -> requests.Response:
        return self._request("POST", "import", json=payload)

    def build_cml_topology(self, topology: dict) -> None:
        lab_info = CreateLabResponse.from_dict(self._load_cml_topology(topology).json())
        self._start_lab(lab_info.id)


def load_topology_from_yaml() -> dict:
    """
    Load the topology from a YAML file.

    Args:
        None
    """
    try:
        with open("build/cml_infrastructure.yml", "r") as f:
            topology = yaml.safe_load(f)
    except Exception as e:
        raise Exception("Error trying to load from cml_infrastructure.yml. Error=%s", e)

    return topology


def main() -> None:
    topology: dict = load_topology_from_yaml()
    CML().build_cml_topology(topology)


if __name__ == "__main__":
    main()
