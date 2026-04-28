"""
Storage service - handles file uploads to local or S3-compatible storage.
"""

import logging
import os
from pathlib import Path
from typing import Optional
import boto3
from botocore.config import Config as BotoConfig

from ..config import Config, get_config

logger = logging.getLogger(__name__)


class StorageService:
    """Service for file storage operations."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or get_config()
        self._s3_client = None

    @property
    def s3_client(self):
        """Lazy initialization of S3 client."""
        if self._s3_client is None and self.config.storage_provider == "s3":
            try:
                self._s3_client = boto3.client(
                    "s3",
                    aws_access_key_id=self.config.s3_access_key_id,
                    aws_secret_access_key=self.config.s3_secret_access_key,
                    endpoint_url=self.config.s3_endpoint_url,
                    region_name=self.config.s3_region_name,
                    config=BotoConfig(signature_version="s3v4"),
                )
                logger.info("S3 client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize S3 client: {e}")
                raise
        return self._s3_client

    async def upload_file(self, local_path: Path, remote_filename: str) -> Optional[str]:
        """
        Upload a file to the configured storage provider.
        Returns the public URL or local path.
        """
        if self.config.storage_provider == "local":
            logger.debug(f"Using local storage for {remote_filename}")
            return f"/clips/{remote_filename}"

        if not local_path.exists():
            logger.error(f"Local file not found: {local_path}")
            return None

        try:
            # For R2/S3, we upload to the bucket
            logger.info(f"Uploading {local_path} to S3 bucket {self.config.s3_bucket} as {remote_filename}")
            
            # Use run_in_executor if this were a high-traffic async app, 
            # but for background workers boto3 is fine in the thread.
            # We'll use the synchronous boto3 client here.
            self.s3_client.upload_file(
                str(local_path),
                self.config.s3_bucket,
                remote_filename,
                ExtraArgs={"ContentType": "video/mp4"}
            )
            
            # Construct public URL
            if "r2.cloudflarestorage.com" in (self.config.s3_endpoint_url or ""):
                # Cloudflare R2 public URL pattern varies, but usually it's a custom domain
                # or a specific R2 public bucket URL. 
                # If no custom domain is provided, we can't easily guess it.
                # However, many users use a public bucket URL.
                # For now, let's return a placeholder or the endpoint-based URL if possible.
                # Actually, R2 public URLs usually look like: https://pub-<hash>.r2.dev/<filename>
                # But it's better if the user provides a BASE_URL for public access.
                public_base_url = os.getenv("STORAGE_PUBLIC_BASE_URL")
                if public_base_url:
                    return f"{public_base_url.rstrip('/')}/{remote_filename}"
                
                # Fallback to endpoint url + bucket + filename (may not work for R2 without auth)
                return f"{self.config.s3_endpoint_url}/{self.config.s3_bucket}/{remote_filename}"
            
            # Standard S3 public URL
            return f"{self.config.s3_endpoint_url}/{self.config.s3_bucket}/{remote_filename}"

        except Exception as e:
            logger.error(f"Failed to upload file to S3: {e}")
            return None

    def get_public_url(self, filename: str) -> str:
        """Get the public URL for a filename."""
        if self.config.storage_provider == "local":
            return f"/clips/{filename}"
        
        public_base_url = os.getenv("STORAGE_PUBLIC_BASE_URL")
        if public_base_url:
            return f"{public_base_url.rstrip('/')}/{filename}"
            
        return f"{self.config.s3_endpoint_url}/{self.config.s3_bucket}/{filename}"
