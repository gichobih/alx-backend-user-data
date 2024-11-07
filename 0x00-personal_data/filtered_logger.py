#!/usr/bin/env python3
"""
Module for handling and obfuscating sensitive personal data in log messages.
"""

from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """Returns log message with specified fields obfuscated"""
    pattern = f"({'|'.join(map(re.escape, fields))})=.*?{re.escape(separator)}"
    return re.sub(pattern, f"\\1={redaction}{separator}", message)
