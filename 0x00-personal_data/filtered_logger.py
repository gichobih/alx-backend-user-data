#!/usr/bin/env python3
"""
Module for handling and obfuscating sensitive personal data in log messages.
"""

from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscates specific fields in a log message.

    Args:
        fields (List[str]): A list of field names to be obfuscated.
        redaction (str): The string to replace field values with.
        message (str): The log message containing fields to obfuscate.
        separator (str): The separator that delimits fields in the log message.

    Returns:
        str: The log message with specified fields obfuscated.
    """
    pattern = f"({'|'.join(map(re.escape, fields))})=.*?{re.escape(separator)}"
    return re.sub(pattern, f"\\1={redaction}{separator}", message)
