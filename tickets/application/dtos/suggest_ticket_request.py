from dataclasses import dataclass


@dataclass(frozen=True)
class SuggestTicketRequest:
    problem_description: str

    def __post_init__(self) -> None:
        if not self.problem_description.strip():
            raise ValueError("Problem description is required")
