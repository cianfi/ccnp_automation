import argparse
import os
import time
from pathlib import Path

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
        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            response_body = response.text.strip()
            if response_body:
                raise requests.HTTPError(
                    f"{error} CML response: {response_body[:1000]}",
                    response=response,
                ) from error
            raise
        return response

    def _authenticate(self) -> requests.Response:
        return self._request(
            "POST",
            "authenticate",
            json={"username": self._username, "password": self._password},
        )

    def _start_lab(self, lab_id: str) -> requests.Response:
        return self._request("PUT", f"labs/{lab_id}/start")

    def _stop_lab(self, lab_id: str) -> requests.Response:
        return self._request("PUT", f"labs/{lab_id}/stop")

    def _delete_lab(self, lab_id: str) -> requests.Response:
        return self._request("DELETE", f"labs/{lab_id}")

    def _wipe_lab(self, lab_id: str) -> requests.Response:
        return self._request("PUT", f"labs/{lab_id}/wipe")

    def _wait_for_lab_state(
        self, lab_id: str, expected_states: set[str], timeout: float = 120
    ) -> str:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            state = self._request("GET", f"labs/{lab_id}/state").json()
            if not isinstance(state, str):
                raise TypeError("Unexpected response while retrieving a CML lab state.")
            if state in expected_states:
                return state
            time.sleep(2)

        expected_state_names = ", ".join(sorted(expected_states))
        raise TimeoutError(
            f"CML lab {lab_id} did not reach {expected_state_names} within {timeout} seconds."
        )

    def _wait_for_nodes_to_boot(self, lab_id: str, timeout: float = 300) -> None:
        node_ids = self._request("GET", f"labs/{lab_id}/nodes").json()
        if not isinstance(node_ids, list) or not all(
            isinstance(node_id, str) for node_id in node_ids
        ):
            raise TypeError("Unexpected response while retrieving CML lab nodes.")

        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            states = []
            for node_id in node_ids:
                response = self._request("GET", f"labs/{lab_id}/nodes/{node_id}/state")
                state = response.json()
                if isinstance(state, dict):
                    state = state.get("state")
                if not isinstance(state, str):
                    raise TypeError("Unexpected response while retrieving a CML node state.")
                states.append(state)

            if all(state == "BOOTED" for state in states):
                return
            time.sleep(2)

        raise TimeoutError(f"CML lab {lab_id} nodes did not boot within {timeout} seconds.")

    def _list_labs(self) -> list[dict]:
        labs = self._request("GET", "labs").json()
        if isinstance(labs, dict):
            labs = labs.get("labs", [])

        if not isinstance(labs, list):
            raise TypeError("Unexpected response while listing CML labs.")

        lab_records = []
        for lab in labs:
            if isinstance(lab, dict):
                lab_records.append(lab)
                continue

            if not isinstance(lab, str):
                raise TypeError("Unexpected lab entry while listing CML labs.")

            lab_details = self._request("GET", f"labs/{lab}").json()
            if not isinstance(lab_details, dict):
                raise TypeError("Unexpected response while retrieving a CML lab.")

            lab_record = lab_details.get("lab", lab_details)
            if not isinstance(lab_record, dict):
                raise TypeError("Unexpected CML lab metadata.")

            lab_record = dict(lab_record)
            lab_record.setdefault("id", lab)
            lab_records.append(lab_record)

        return lab_records

    def _load_cml_topology(self, payload: dict) -> requests.Response:
        return self._request("POST", "import", json=payload)

    def build_cml_topology(self, topology: dict) -> None:
        lab_info = CreateLabResponse.from_dict(self._load_cml_topology(topology).json())
        self._start_lab(lab_info.id)
        self._wait_for_nodes_to_boot(lab_info.id)

    def replace_cml_topology(self, topology: dict) -> None:
        lab = topology.get("lab", {})
        lab_title = lab.get("title")
        if not lab_title:
            raise ValueError("CML topology must define lab.title.")

        for existing_lab in self._list_labs():
            existing_title = existing_lab.get("title") or existing_lab.get("lab_title")
            if existing_title != lab_title:
                continue

            lab_id = existing_lab.get("id")
            if not lab_id:
                raise ValueError("CML lab is missing its id.")

            state = existing_lab.get("state")
            if state not in {"STOPPED", "CREATED", "DEFINED_ON_CORE"}:
                self._stop_lab(lab_id)
                state = self._wait_for_lab_state(
                    lab_id, {"STOPPED", "DEFINED_ON_CORE"}
                )
            if state == "STOPPED":
                self._wipe_lab(lab_id)
                self._wait_for_lab_state(lab_id, {"CREATED", "DEFINED_ON_CORE"})
            self._delete_lab(lab_id)

        self.build_cml_topology(topology)


def load_topology_from_yaml() -> dict:
    """
    Load the topology from a YAML file.

    Args:
        None
    """
    topology_path = Path(__file__).with_name("cml_infrastructure.yml")
    try:
        with topology_path.open("r", encoding="utf-8") as f:
            topology = yaml.safe_load(f)
    except (OSError, yaml.YAMLError) as error:
        raise RuntimeError("Error trying to load cml_infrastructure.yml.") from error

    return topology


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--replace",
        action="store_true",
        help="delete the existing lab with the YAML title before importing it",
    )
    args = parser.parse_args()

    topology: dict = load_topology_from_yaml()
    cml = CML()
    if args.replace:
        cml.replace_cml_topology(topology)
    else:
        cml.build_cml_topology(topology)


if __name__ == "__main__":
    main()
