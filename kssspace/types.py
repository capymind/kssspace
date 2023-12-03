"""
Types.
"""
from typing import Any, NewType

type GiantRecord = dict[str, Any]
type TagName = str
type TagId = int


InvalidData = NewType("InvalidData", dict[str, Any])
