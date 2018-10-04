import logging
import click_log as clog

# -- Logger def.
logger = logging.getLogger(__name__)
clog.basic_config(logger)
