from typing import Type

import tldextract

from .base import BaseHandler
from .youtube import YoutubeHandler

__all__ = ["get_handler", "UnsupportedDomainError", "BaseHandler", "YoutubeHandler"]


class UnsupportedDomainError(Exception):
    """Raised when domain is not supported by API"""

    pass


_handlers_mapping: dict[str, Type[BaseHandler]] = {"youtube": YoutubeHandler}


def get_handler(url: str) -> Type[BaseHandler]:
    domain = tldextract.extract(url).domain
    if not domain:
        raise ValueError("Invalid URL")
    handler = _handlers_mapping.get(domain)
    if not handler:
        raise UnsupportedDomainError(f"Domain '{domain}' is not supported")
    if not handler.is_valid_url(url):
        raise ValueError("Invalid URL")
    return handler
