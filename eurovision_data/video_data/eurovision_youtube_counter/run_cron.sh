#!/bin/sh
source /opt/euro_counter/euro_counter_env/bin/activate
python /opt/euro_counter/eurovision_data/video_data/eurovision_youtube_counter/run_cron.py & >> /tmp/bash_cron_log.txt
