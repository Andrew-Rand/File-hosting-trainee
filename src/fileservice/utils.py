import hashlib
import os
from typing import List, Dict, Any, Union

import magic
from django.core.files.uploadedfile import UploadedFile
from django.core.mail import send_mail

from src.config import settings
from src.fileservice.constants import ALLOWED_FILETYPES


def calculate_hash_md5(file_path: str) -> str:
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def make_chunk_dir_path(temp_storage_path: str, user_id: str, data: Dict[str, Any]) -> str:
    user_dir_path = os.path.join(temp_storage_path, user_id)
    chunks_dir_path = os.path.join(user_dir_path, data.get('identifier'))
    return chunks_dir_path


def make_chunk_paths(chunks_dir_path: str, data: Dict[str, Any]) -> List[str]:

    filename = data.get('filename')
    total_chunks = data.get('total_chunk')

    chunk_paths = [
        os.path.join(chunks_dir_path, get_chunk_name(filename, x))
        for x in range(1, total_chunks + 1)
    ]
    return chunk_paths


def is_all_chunk_uploaded(chunk_paths: List[str]) -> bool:
    return all([os.path.exists(p) for p in chunk_paths])


def get_chunk_name(uploaded_filename: str, chunk_number: int) -> str:
    return f'{uploaded_filename}_part_{chunk_number}'


def save_file(target_file_path: str, chunk_paths: List[str]) -> None:
    with open(target_file_path, 'ab') as target_file:
        for stored_chunk_file_name in chunk_paths:
            stored_chunk_file = open(stored_chunk_file_name, 'rb')
            target_file.write(stored_chunk_file.read())
            stored_chunk_file.close()
            os.unlink(stored_chunk_file_name)
    target_file.close()


def send_warning_email_to_user(user_email: str, message: str) -> None:
    send_mail('Warning', message, settings.DEFAULT_FROM_EMAIL, (user_email,))


def is_filetype_valid(file: Union[UploadedFile, str]) -> bool:
    if isinstance(file, UploadedFile):
        file = file.read(2048)
        file_type = magic.from_buffer(file, mime=True)
    elif isinstance(file, str):
        file_type = magic.from_file(file, mime=True)
    else:
        return False
    return file_type in ALLOWED_FILETYPES
