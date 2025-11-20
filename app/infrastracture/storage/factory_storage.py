from app.domain import StorageRepository
from app.infrastracture import LocalStorageRepository
from app.infrastracture.storage import S3StorageRepository
from app.settings import StorageType, settings


def factory_storage_repository(storage_type: StorageType) -> StorageRepository:
    """Create storage repository based on settings."""
    if settings.storage_type == StorageType.S3:
        if not settings.aws_s3_bucket:
            raise ValueError("aws_s3_bucket is required when using S3 storage")
        return S3StorageRepository(
            bucket_name=settings.aws_s3_bucket,
            region=settings.aws_region,
            access_key_id=settings.aws_access_key_id,
            secret_access_key=settings.aws_secret_access_key,
        )
    return LocalStorageRepository(data_dir=settings.data_dir)
