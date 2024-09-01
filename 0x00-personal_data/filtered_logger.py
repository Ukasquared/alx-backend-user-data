#!/usr/bin/env python3
""" the log message obfuscated """
import re
import logging
import time


def filter_datum(fields, redaction, message, separator):
    """ returns an obfuscated log message"""
    for item in fields:
        message = re.sub(rf"\b{item}[^{separator}]*", 
                    f"{item}={redaction}", message)
    return(message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        """ base class"""
        self.field = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ format log record """
        new_message = filter_datum(self.field, self.REDACTION, record.getMessage(), self.SEPARATOR)
        self.FORMAT = self.FORMAT % {"name": record.name, "levelname":record.levelname, "asctime": f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record.created))},{int(record.msecs):03d}', "message": new_message}
        return self.FORMAT
