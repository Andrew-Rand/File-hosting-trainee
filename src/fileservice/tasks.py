import os
import shutil
from datetime import datetime, timedelta
from typing import Dict, Any

from src.accounts.models import User
from src.basecore.custom_error_handler import BadRequestError
from src.etl import celery_app
from src.fileservice.models import FileStorage, File
from src.fileservice.models.file_storage import TEMP_STORAGE
from src.fileservice.utils import get_chunk_name, is_all_chunk_uploaded, save_file, calculate_hash_md5


CHUNK_EXPIRATION_TIME = timedelta(days=7)


@celery_app.task
def task_build_file(user_id: str, temp_storage_id: str, permanent_storage_id: str, data: Dict[str, Any]) -> None:

    identifier = data.get('identifier')
    filename = data.get('filename')
    total_chunks = data.get('total_chunk')

    user = User.objects.get(id=user_id)
    temp_storage = FileStorage.objects.get(id=temp_storage_id)
    permanent_storage = FileStorage.objects.get(id=permanent_storage_id)

    # make temp directory
    user_dir_path = os.path.join(temp_storage.destination, str(user.id))
    chunks_dir_path = os.path.join(user_dir_path, identifier)

    # check if the upload is complete
    chunk_paths = [
        os.path.join(chunks_dir_path, get_chunk_name(filename, x))
        for x in range(1, total_chunks + 1)
    ]
    if not is_all_chunk_uploaded(chunk_paths):
        raise BadRequestError('There aren`t all chunks for this file. Try to continue upload chunks')

    # create final file from all chunks
    user_storage_path = os.path.join(permanent_storage.destination, str(user.id))
    os.makedirs(user_storage_path, 0o777, exist_ok=True)
    target_file_path = os.path.join(user_storage_path, filename)
    save_file(target_file_path, chunk_paths)
    os.rmdir(chunks_dir_path)

    file_hash = calculate_hash_md5(target_file_path)

    File.create_model_object(user, file_hash, permanent_storage, target_file_path, data)


@celery_app.task
def delete_unbuilt_chunks() -> None:
    temp_storage = FileStorage.objects.get(type=TEMP_STORAGE)
    temp_storage_path = temp_storage.destination
    user_dirs = os.listdir(temp_storage_path)
    if user_dirs:
        for user_dir in user_dirs:
            dirpath_to_rm = os.path.join(temp_storage_path, user_dir)
            st = os.stat(dirpath_to_rm)
            mtime = st.st_mtime
            time_of_dir_mod = datetime.fromtimestamp(mtime)
            if datetime.utcnow() - time_of_dir_mod > CHUNK_EXPIRATION_TIME:
                shutil.rmtree(dirpath_to_rm, ignore_errors=True)
