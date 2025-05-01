from app.cfg.minio.minio_buckets import _MinioBuckets
from app.cfg.settings import settings


class MinioManager:
    def __init__(self, bucket: _MinioBuckets = _MinioBuckets.AVATARS):
        self._MINIO_STORAGE_ENDPOINT = ...
        self._MINIO_SECRET_KEY = ...
        self._MINIO_ACCESS_KEY = ...
        self._MINIO_BUCKET_TYPE = bucket

    async def upload_data(self):
        pass

    async def download_data(self):
        ...