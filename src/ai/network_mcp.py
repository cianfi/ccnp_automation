from pathlib import Path
import json
from typing import Any

from fastmcp import FastMCP
from genie.testbed import load

devices = load(str(Path(__file__).parent / "testbed.yaml"))

mcp = FastMCP(
    name="Network MCP Server",
    instructions="This is an MCP server to get info on network devices",
)


@mcp.resource(uri="resource://devices")
def get_devices() -> str:
    inventory = []

    for name, device in devices.devices.items():
        inventory.append(
            {
                "name": name,
                "os": device.os,
                "type": device.type,
                "connections": {
                    connection_name: {
                        "protocol": config.get("protocol"),
                        "ip_address": config.get("ip_address"),
                        "port": config.get("port"),
                    }
                    for connection_name, config in device.connections.items()
                },
            }
        )

    return json.dumps(inventory, indent=2)


@mcp.tool(name="get_ip_interface_brief")
def ip_interface_brief(device_name: str) -> Any:
    device = devices.devices[device_name]

    device.connect(via="cli", log_stdout=False)
    output = device.execute("show ip interface brief")
    device.disconnect()
    return output


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port="8000")
