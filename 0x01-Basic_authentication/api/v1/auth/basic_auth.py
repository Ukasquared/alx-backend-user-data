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

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """ returns username and password"""
        if not decoded_base64_authorization_header:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if r":" not in decoded_base64_authorization_header:
            return (None, None)
        value = re.split(':', decoded_base64_authorization_header)
        return tuple(value)

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ returns username based
        on his email and password
        """
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None
