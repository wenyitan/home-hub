import logging as logger

log_filename = 'app.log'

logger.basicConfig(
    filename=log_filename,
    level=logger.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)