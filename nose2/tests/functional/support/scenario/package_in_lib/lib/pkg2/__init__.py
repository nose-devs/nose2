import logging

log = logging.getLogger(__name__)

def get_one():
    log.debug("Returning %s", 1)
    return 1
