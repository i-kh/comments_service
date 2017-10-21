import os
import uuid
from json import dumps

from celery.result import allow_join_result

from comments_service.celery_config import app
from comments_service.comment.notify import send_notification
from comments_service.constants import JSON
from comments_service.settings import MEDIA_ROOT, MEDIA_URL


@app.task
def save_history_to_file(history, ext=None, *args, **kwargs):
    ext = ext or JSON
    ext_dict = {JSON: dumps}
    data_processing_function = ext_dict.get(ext, None)
    if data_processing_function:
        history = data_processing_function(history, *args, **kwargs)
    file_name = '{random_name}.{ext}'.format(random_name=uuid.uuid4(), ext=ext)
    with open(os.path.join(MEDIA_ROOT, file_name), 'w+') as f:
        f.write(history)
    return '{media_url}{file_name}'.format(media_url=MEDIA_URL,
                                           file_name=file_name)


@app.task
def obtain_result_and_notify(task_id, param_name):
    result = save_history_to_file.AsyncResult(task_id)
    with allow_join_result():
        send_notification({param_name: result.get()})
