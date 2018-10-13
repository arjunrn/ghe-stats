import logging

from github import Github

logger = logging.getLogger(__name__)


def client(token: str, api_url: str):
    logger.debug("Creating Github Client with URL: %s and Token: %s", api_url, token[0:4])
    g = Github(base_url=api_url, login_or_token=token)
    return g
