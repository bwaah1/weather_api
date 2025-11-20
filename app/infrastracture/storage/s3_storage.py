import json
from datetime import UTC, datetime
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

from app.domain.repositories.storage import StorageRepository
from app.domain.weather import Weather


class S3StorageRepository(StorageRepository):
    def __init__(
        self,
        bucket_name: str,
        region: str = "us-east-1",
        access_key_id: str | None = None,
        secret_access_key: str | None = None,
    ) -> None:
        self.bucket_name = bucket_name
        self.region = region

        session_kwargs = {"region_name": region}
        if access_key_id and secret_access_key:
            session_kwargs["aws_access_key_id"] = access_key_id
            session_kwargs["aws_secret_access_key"] = secret_access_key

        session = boto3.Session(**session_kwargs)
        self.s3_client = session.client("s3")

    async def save(self, city: str, weather: Weather) -> Path:
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        filename = f"{city}_{timestamp}.json"
        s3_key = filename

        weather_json = json.dumps(weather.model_dump(mode="json"), indent=2)

        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=weather_json.encode("utf-8"),
                ContentType="application/json",
            )

            return Path(f"s3://{self.bucket_name}/{s3_key}")
        except ClientError as e:
            raise RuntimeError(f"Failed to upload to S3: {e}") from e
