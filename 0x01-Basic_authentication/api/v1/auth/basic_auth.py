#!/usr/bin/env python3
""" Basic Authentication
Module """
from api.v1.auth.auth import Auth
import re


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
