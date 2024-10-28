from dataclasses_json import dataclass_json
from dataclasses import dataclass
from datetime import date


@dataclass_json
@dataclass
class Animal:
    name: str
    date_of_birth: date
    commands: list[str]
