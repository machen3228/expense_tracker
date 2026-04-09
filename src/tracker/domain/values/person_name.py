import re
from typing import ClassVar

from tracker.domain.errors import ValidationError
from tracker.domain.values.base import Value
from tracker.domain.values.base import value


@value
class PersonName(Value):
    _MIN_LENGTH: ClassVar[int] = 3
    _MAX_LENGTH: ClassVar[int] = 30
    _PERSON_NAME_FMT: ClassVar[re.Pattern[str]] = re.compile(r"^[a-z0-9]+$")

    value: str

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        stripped: str = self.value.strip()
        if not stripped:
            raise ValidationError("Invalid person name: person name must not be empty")

        if len(stripped) < self._MIN_LENGTH:
            raise ValidationError(f"Invalid person name: person name must be at least {self._MIN_LENGTH} characters")

        if len(stripped) > self._MAX_LENGTH:
            raise ValidationError(f"Invalid person name: person name must not exceed {self._MAX_LENGTH} characters")

        if not self._PERSON_NAME_FMT.match(stripped):
            raise ValidationError("Invalid person name: person name contains invalid characters")

        object.__setattr__(self, "value", stripped)
