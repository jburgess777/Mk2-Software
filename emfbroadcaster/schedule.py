#!/usr/bin/env python
import logging
import json
import requests
import struct
import sys
import binascii
import time
import tinypacks
import re

def show_usage_message():
    print "Usage: ./schedule.py 2014-08-29 40963"
    print "Usage: ./schedule.py 2014-08-30 40964"
    print "Usage: ./schedule.py 2014-08-31 40965"
    sys.exit(1)

if len(sys.argv) < 3:
    show_usage_message();

day = sys.argv[1];
if not re.match(r"\d\d\d\d-\d\d-\d\d", day):
    show_usage_message()

rid = int(sys.argv[2])

config = json.load(open('../etc/config.json'))

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('schedule');

logger.info("Updating schedule for day %s and rid %d", day, rid);

type_ids = {
    "lecture": 1,
    "installation": 2,
    "workshop": 3,
    "other": 4
}

resp = requests.get(url=config['scheduleUrl'])
schedule_json = json.loads(resp.text);

print schedule_json;

talks = []
for event in schedule_json['conference_events']['events']:

    if 'start_time' in event:
        location_id = event['room']['id']
        start_timestamp = int(round(time.mktime(time.strptime(event['start_time'], "%Y-%m-%dT%H:%M:%SZ"))));
        end_timestamp = int(round(time.mktime(time.strptime(event['end_time'], "%Y-%m-%dT%H:%M:%SZ"))));
        matches_day = (event['start_time'][0:10] == day)
    else:
        location_id = 0
        start_timestamp = 0
        end_timestamp = 0
        matches_day = False
        logger.info("Talk without start_time: %s", event)

    type_id = type_ids[event['type']]

    speaker = "";
    if 'speaker' in event:
        speaker = event['speaker']['full_public_name']

    if matches_day:
        talks.append({
            "location_id": location_id,
            "type_id": type_id,
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
            "speaker": speaker,
            "title": event['title'],
            "abstract": event['abstract']
        })

packed = tinypacks.pack(len(talks));
for talk in talks:
    packed += tinypacks.pack(talk['location_id']);
    packed += tinypacks.pack(talk['type_id']);
    packed += tinypacks.pack(talk['start_timestamp']);
    packed += tinypacks.pack(talk['end_timestamp']);
    packed += tinypacks.pack(talk['speaker']);
    packed += tinypacks.pack(talk['title']);

print binascii.hexlify(packed)
logger.info("Content length: %d", len(packed))

# Update content
logger.info("Sending content...")
params = dict( rid=rid )
response = requests.post(url=config['mcpBroadcastEndpoint'], params=params, data=packed)

logger.info("Response from MCP: %s", response)

logger.info("All done")