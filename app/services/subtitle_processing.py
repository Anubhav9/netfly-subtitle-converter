import json
import logging
import requests
import cv2
import boto3

from app.utils.merge_subtitles import merge_subtitles


class subtitle_processing:
    def __init(self):
        pass

    def get_frames_from_video(self, video_path):
        cap = cv2.videoCapture(video_path)
        frame_count = 0
        fps = cap.get(cv2.CAP_PROP_FPS)
        logging.info(f"Frames per second for the video is:: {fps}")
        frames = []
        while True:
            ret, frame = cap.read()
            if ret:
                logging.info(f"Frame {frame_count} is read")
                if frame_count % fps == 0:
                    logging.info(f"Frame count:: {frame_count} needs to be stored and processed")
                    frames.append(frame)
                frame_count = frame_count + 1
                pass
            else:
                logging.info("Video processing completed")

        return frames

    def store_frames_in_s3_bucket(self, frames, bucket_name, key_prefix):
        logging.info(f"Storing frames in s3 bucket:: {bucket_name}")
        s3_client = boto3.client("s3", region_name="ap-northeast-1")
        for i in range(0, len(frames)):
            logging.info(f"Uploading frame:: {i} to s3 bucket")
            key_name = key_prefix + "/" + str(i) + ".jpg"
            try:
                s3_client.upload_fileobj(frames[i], Bucket=bucket_name, Key=key_name)
            except Exception as e:
                logging.error(f"Error Uploading frame: {i} to S3 Bucket. Error is:: {e}")
        logging.info(f"Frames uploaded to s3 bucket:: {bucket_name} successfully")

    def get_text_from_images_via_google_vision(self, bucket_name, key_name):
        s3_client = boto3.client("s3", region_name="ap-northeast-1")
        img_object = s3_client.get_object(Bucket=bucket_name, Key=key_name)
        if img_object is None:
            logging.error(f"Image object not found in s3 bucket:: {bucket_name}")
            return None
        img_data = img_object["Body"].read()
        logging.info(f"Successfully read Image Data from S3 Bucket")
        response = requests.post("https://vision.googleapis.com/v1/images:annotate?key=API_KEY", json={
            "requests": [
                {
                    "image": {
                        "content": img_data
                    },
                    "features": [
                        {
                            "type": "TEXT_DETECTION"
                        }
                    ]
                }
            ]
        })
        if response.status_code != 200:
            logging.error(f"Error in Google Vision API Call. Response code is:: {response.status_code}")
            return None
        else:
            logging.info(f"API Call to Google Vision API successfully made")
            body = response.json()["fullTextAnnotation"]["text"]
            body=body.replace("\n"," ")
            logging.info(f"Text received from Google Vision API is::{body}")
            return body

    def get_translation_via_aws_translate(self, text, source_language, target_language):
        translate_client = boto3.client("translate", region_name="ap-northeast-1")
        translated_text = translate_client.translate_text(Text=text, SourceLanguageCode=source_language,
                                                          TargetLanguageCode=target_language)
        if translated_text is None:
            logging.error(f"Error in translating text::{text}")
            return None
        else:
            target_text = translated_text["TranslatedText"]
            logging.info(f"Translated Text is:: {target_text}")
            return translated_text

    def process_video(self,video_path,bucket_name):
        logging.info(f"Starting Step 1: Getting frames from video")
        frame_list=self.get_frames_from_video(video_path)
        logging.info(f"Step 1 completed successfully")
        logging.info(f"Starting Step 2: Storing frames in s3 bucket")
        key_prefix=video_path.split(".")[0]
        logging.info("Inside bucket, frames will be stored in the folder :: {key_prefix}")
        self.store_frames_in_s3_bucket(frame_list,bucket_name,key_prefix)
        logging.info(f"Step 2 completed successfully")
        logging.info(f"Starting Step 3: Getting text from images via Google Vision API")
        start_time=0
        end_time=1
        language_mapping_list=[]
        for i in range(0,len(frame_list)):
            key_name=key_prefix+"/"+str(i)+".jpg"
            text_from_vision_api=self.get_text_from_images_via_google_vision(bucket_name,key_name)
            translated_text_from_aws_translate=self.get_translation_via_aws_translate(text_from_vision_api,"ja","en")
            language_mapping_list.append({"start_time":start_time,"end_time":end_time,"original_text":text_from_vision_api,"translated_text":translated_text_from_aws_translate})
            start_time=start_time+1
            end_time=end_time+1
        logging.info(f"Step 3 completed successfully")
        logging.info(f"We are Sanitising the received JSON now")
        logging.info(f"Starting Step 4: Sanitising the JSON")
        for i in range(0,len(language_mapping_list)):
            if language_mapping_list[i]["translated_text"]=="":
                if(i==0):
                    language_mapping_list[i]["translated_text"]="Hello, This project is powered by github.com/Anubhav9"
                    language_mapping_list[i]["original_text"]="こんにちは、このプロジェクトはgithub.com/Anubhav9によって提供されています"
                else:
                    language_mapping_list[i]["translated_text"]=language_mapping_list[i-1]["translated_text"]
                    language_mapping_list[i]["original_text"]=language_mapping_list[i-1]["original_text"]
        logging.info(f"Step 4 completed successfully")
        logging.info(f"Starting Step 5: Merging the subtitles")
        merged_subtitles_list=merge_subtitles(language_mapping_list)
        merged_subtitles_list=json.dumps(merged_subtitles_list)
        logging.info(f"Printing Merged Subtitles list :: {merged_subtitles_list}")
        return merged_subtitles_list



