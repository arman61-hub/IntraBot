from pathlib import Path
from typing import Dict, List

BASE_DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "Fintech-data"

# Role → allowed document folders (PDF compliant)
ROLE_DOCUMENT_MAP: Dict[str, List[str]] = {
    "finance": ["finance", "general"],
    "marketing": ["marketing", "general"],
    "hr": ["hr", "general"],
    "engineering": ["engineering", "general"],
    "employees": ["general"],
    "c_level": ["finance", "marketing", "hr", "engineering", "general"],
}


def get_allowed_dirs(role: str) -> List[Path]:
    role = role.lower()
    if role not in ROLE_DOCUMENT_MAP:
        raise ValueError(f"Invalid role: {role}")

    dirs: List[Path] = []
    for folder in ROLE_DOCUMENT_MAP[role]:
        path = BASE_DATA_PATH / folder
        if path.exists():
            dirs.append(path)
            
    return dirs

# Used during preprocessing to attach RBAC metadata.
def roles_for_department(department: str) -> List[str]:
    allowed_roles = []
    for role, folders in ROLE_DOCUMENT_MAP.items():
        if department in folders:
            allowed_roles.append(role)
            
    return sorted(allowed_roles)
