#!/usr/bin/env python3
""" Basic Authentication
Module """
from api.v1.auth.auth import Auth
import re
import base64
from binascii import Error


class BasicAuth(Auth):
    """Basic
    Authentication
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ validate authorization header """
        if not authorization_header:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not re.search(r"^Basic\s", authorization_header):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """decode a base64 string"""
        if not base64_authorization_header:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        decoded = ''
        try:
            decoded = base64.b64decode(base64_authorization_header)
        except Error:
            return None
        return decoded.decode('utf-8')
