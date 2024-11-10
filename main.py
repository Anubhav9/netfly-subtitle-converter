import logging
import os

import boto3
from services.subtitle_processing import subtitle_processing

logging.basicConfig(level=logging.INFO)


def create_translated_json(video_path):
    s3_client = boto3.client("s3", region_name="ap-northeast-1")
    bucket_name = os.environ.get("SUBTITLES_BUCKET_NAME")
    try:
        s3_client.create_bucket(Bucket=bucket_name,
                                CreateBucketConfiguration={'LocationConstraint': 'ap-northeast-1'})
        logging.info(f"Bucket created successfully with name::{bucket_name}")
    except Exception as e:
        logging.warning(f"Bucket already exists with name::{bucket_name}")
        logging.error(f"Printing Exception::{e}")
    subtitle_processing_obj = subtitle_processing()
    subtitle_processing_obj.process_video(video_path, bucket_name)
    return "Finished Processing"
