from dataclasses import dataclass, field


@dataclass
class DataClass:
    name: str
    var: float = field(init=False)

    def __post_init__(self) -> None:
        self.var = 5