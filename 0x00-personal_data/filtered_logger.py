#!/usr/bin/env python3
""" the log message obfuscated """
import re


def filter_datum(fields, redaction, message, separator):
    """ returns an obfuscated log message"""
    for item in fields:
        message = re.sub(rf"\b{item}[^{separator}]*", 
                    f"{item}={redaction}", message)
    return(message)
