from json import dumps
from channels import Group
import logging


logger = logging.getLogger(__name__)


def send_notification(notification):
    logger.info('send_notification. notification = %s', notification)
    Group("notifications").send({'text': dumps(notification)})