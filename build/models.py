from dataclasses import dataclass


@dataclass
class CMLGroups:
    id: str
    permission: str


@dataclass
class CreateLabResponse:
    id: str
    state: str
    created: str
    modified: str
    lab_title: str
    owner: str
    owner_username: str
    owner_fullname: str
    lab_description: str
    node_count: int
    link_count: int
    lab_notes: str
    groups: list[CMLGroups]

    @classmethod
    def from_dict(cls, data: dict) -> "CreateLabResponse":
        return cls(
            id=data.get("id", ""),
            state=data.get("state", ""),
            created=data.get("created", ""),
            modified=data.get("modified", ""),
            lab_title=data.get("lab_title", ""),
            owner=data.get("owner", ""),
            owner_username=data.get("owner_username", ""),
            owner_fullname=data.get("owner_fullname", ""),
            lab_description=data.get("lab_description", ""),
            node_count=data.get("node_count", 0),
            link_count=data.get("link_count", 0),
            lab_notes=data.get("lab_notes", ""),
            groups=[
                CMLGroups(id=g.get("id", ""), permission=g.get("permission", ""))
                for g in data.get("groups", [])
            ],
        )
