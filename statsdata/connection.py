import logging

import psycopg2

logger = logging.getLogger(__name__)


def get_connection(connection_string: str):
    return psycopg2.connect(connection_string)
