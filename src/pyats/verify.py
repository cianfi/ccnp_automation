import sys
from collections import defaultdict

import csv
from genie.libs.conf.testbed import Testbed
from genie.libs.conf.device.ios.device import Device
from genie.testbed import load


def config_parser(device: Device, command: str) -> dict:
    try:
        _config = device.parse(command)
        return _config
    except BaseException as E:
        raise Exception(
            f"There was an error running the command '{command}' on device '{device}'. Error: {E}"
        )


def get_actual_interface_config(device: Device) -> dict[str, dict[str, dict[str, str]]]:
    """
    ...

    Example result:
        {
        "interface": {
            "GigabitEthernet1": {
                "ip_address": "10.209.71.18",
                "interface_is_ok": "YES",
                "method": "NVRAM",
                "status": "up",
                "protocol": "up",
            },
        }
    """
    _raw_interface_config = config_parser(device, "show ip interface brief")
    return _raw_interface_config


def get_actual_interface_description(device: Device) -> dict:
    """
    Returns:
        {
        "interfaces": {
            "GigabitEthernet1": {
                "status": "up",
                "protocol": "up",
                "description": "To Cloud Interface",
            }
        }
    """
    _raw_config = config_parser(device, "show interface description")
    return _raw_config


def mix_actual(config_1: dict, config_2: dict) -> dict:
    for v in config_2.values():
        for int, config in v.items():
            config_1["interface"][int].update({"description": config["description"]})

    return config_1


def csv_loader(source_of_truth_file: str) -> dict[str, dict[str, dict[str, str]]]:
    """
    Loads the Source of Truth CSV file which we will compare to live configurations.
    Returns the following data:
        {
            "router-1": {
                "GigabitEthernet1": {"ip": "10.209.71.18", "description": ""},
                "GigabitEthernet2": {"ip": "unassigned", "description": ""},
                "GigabitEthernet3": {"ip": "unassigned", "description": ""},
                "GigabitEthernet4": {"ip": "unassigned", "description": ""},
                "Loopback0": {"ip": "192.168.3.67", "description": ""},
            }
        }
    """
    device_sot = defaultdict(dict)
    with open(source_of_truth_file, "r") as sot:
        for row in csv.DictReader(sot):
            device_sot[row["device"]][row["interface"]] = {
                "ip": row["ip"],
                "description": row["description"],
            }
    return dict(device_sot)


def load_testbed() -> Testbed:
    _devices: Testbed = load("testbed.yaml")
    return _devices


def compare_sot_to_testbed(sot: dict, live: dict): ...


def ping(device: Device, target: list[str]) -> bool:
    for ip in target:
        try:
            result = device.ping(ip)
            print(result)
        except BaseException as e:
            print(f"Failed to ping: {e}")
            return False
    return True


def main():
    sot = csv_loader("interface_sot.csv")

    devices: Testbed = load_testbed()
    for device in devices:
        if device.name != "router-1":
            continue

        device.connect(log_stdout=False)
        raw_interface_config = get_actual_interface_config(device)
        raw_interface_desc = get_actual_interface_description(device)
        current_config = mix_actual(raw_interface_config, raw_interface_desc)

        compare_sot_to_testbed(current_config, sot)

        # CRITICAL_INFRA = ["10.209.71.18"]
        # can_ping = ping(device, CRITICAL_INFRA)
        # if not can_ping:
        #     print(f"Device {device} cant ping critical infra")


if __name__ == "__main__":
    main()
