import re
from collections.abc import Iterable

_COMPANY_IDENTIFIER = re.compile(
    r"(?<![A-Za-z0-9-])([A-Za-z0-9][A-Za-z0-9-]*-(?:domain|site)-verification)\s*=",
    re.IGNORECASE,
)

def extract_company_identifiers(records: Iterable[str]) -> list[str]:
    identifiers: list[str] = []
    seen: set[str] = set()

    for record in records:
        for match in _COMPANY_IDENTIFIER.finditer(record):
            identifier = match.group(1).lower()
            if identifier not in seen:
                seen.add(identifier)
                identifiers.append(identifier)

    return identifiers