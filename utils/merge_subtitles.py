import logging


def merge_subtitles(subtitles_list):
    logging.warning(f"The size of the subtitle list that we have got is :: {len(subtitles_list)}")
    merged_subtitle_list = []
    start_time_list = []
    end_time_list = []
    break_point = []
    for i in range(1, len(subtitles_list)):
        logging.info(f"The current iterable is :: {str(i)}")
        current_subtitle = subtitles_list[i]["translated_text"]
        previous_subtitle = subtitles_list[i - 1]["translated_text"]
        if current_subtitle != previous_subtitle:
            if i == len(subtitles_list) - 1:
                logging.info("We are at the last subtitle, hence handling it explicitly")
                new_json = {
                    "start_time": subtitles_list[i]["start_time"],
                    "end_time": subtitles_list[i]["end_time"],
                    "translated_text": subtitles_list[i]["translated_text"]
                }
                merged_subtitle_list.append(new_json)
            else:
                logging.info("Both the subtitles post comparison were found to be different")
                start_time_list.append(subtitles_list[i - 1]["start_time"])
                end_time_list.append(subtitles_list[i]["start_time"])
                new_json = {
                    "start_time": min(start_time_list),
                    "end_time": max(end_time_list),
                    "translated_text": subtitles_list[i - 1]["translated_text"],
                }
                merged_subtitle_list.append(new_json)
                start_time_list.clear()
                end_time_list.clear()
                break_point.clear()
        else:
            logging.info("Both the subtitles are found to be similar")
            break_point.append(i)
            if i == len(subtitles_list) - 1:
                logging.info(
                    "Since we have reached the end of the subtitle [ same ] , hence we need to handle it explicitly")
                new_json = {
                    "start_time": min(break_point),
                    "end_time": len(subtitles_list),
                    "translated_text": subtitles_list[i]["translated_text"]
                }
                merged_subtitle_list.append(new_json)
            else:
                start_time_list.append(subtitles_list[i - 1]["start_time"])
                end_time_list.append(subtitles_list[i - 1]["end_time"])

    return merged_subtitle_list
