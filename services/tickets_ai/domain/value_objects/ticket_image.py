from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class Image:
    filename: str
    content_type: str
    content: bytes

    valid_content_types: ClassVar[frozenset[str]] = frozenset({
        "image/jpeg", "image/png", "image/jpg", "image/webp",
    })

    def __post_init__(self):
        if not isinstance(self.filename, str):
            raise TypeError("filename must be a string")
        if not isinstance(self.content_type, str):
            raise TypeError("content_type must be a string")
        if not isinstance(self.content, bytes):
            raise TypeError("content must be bytes")
        if self.content_type not in self.valid_content_types:
            raise ValueError(f"Invalid content type: {self.content_type}")
        if not self.content:
            raise ValueError("Image content cannot be empty")
