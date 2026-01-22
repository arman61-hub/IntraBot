from pathlib import Path
from typing import Dict, List, Set

BASE_DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "Fintech-data"

# Role → allowed document folders
ROLE_DOCUMENT_MAP: Dict[str, List[str]] = {
    "finance": ["finance"],
    "marketing": ["marketing"],
    "hr": ["hr"],
    "engineering": ["engineering"],
    "employees": ["general"],
    "c_level": ["finance", "marketing", "hr", "engineering", "general"],
}

# Explicit role hierarchy
ROLE_HIERARCHY: Dict[str, List[str]] = {
    "c_level": ["finance", "marketing", "hr", "engineering", "employees"],
}


def get_allowed_dirs(role: str) -> List[Path]:
    role = role.lower()
    if role not in ROLE_DOCUMENT_MAP:
        raise ValueError("Invalid role")

    dirs: List[Path] = []
    for folder in ROLE_DOCUMENT_MAP[role]:
        path = BASE_DATA_PATH / folder
        if path.exists():
            dirs.append(path)
    return dirs


# Returns roles allowed to access a given department. Used during preprocessing to attach metadata.
def roles_for_department(department: str) -> List[str]:
    allowed_roles = []

    for role, departments in ROLE_DOCUMENT_MAP.items():
        if department in departments:
            allowed_roles.append(role)

    return sorted(allowed_roles)


# Returns the set of roles a user effectively has, considering role hierarchy.
def get_effective_roles(role: str) -> Set[str]:
    role = role.lower()
    effective = {role}

    inherited = ROLE_HIERARCHY.get(role, [])
    effective.update(inherited)

    return effective
