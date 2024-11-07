#!/usr/bin/env python3
"""
Module for handling Personal Data
"""

from typing import List
import re

def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Obfuscates specified fields in a log message."""
    pattern = f"({'|'.join(fields)})=.*?{separator}"
    return re.sub(pattern, f"\\1={redaction}{separator}", message)

