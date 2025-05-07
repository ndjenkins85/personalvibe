# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Placeholder auth system.

For the MVP we rely on signed cookies and a single hard-coded user.
Swap with proper OAuth or Firebase once the rest of the platform
stabilises.
"""

from dataclasses import dataclass


@dataclass
class User:
    id: str
    email: str
    display_name: str


# Global dev user
DEV_USER = User(id="0000", email="dev@local", display_name="Dev User")
