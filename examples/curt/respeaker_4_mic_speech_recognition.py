""" 
This example demonstrates the use of the ResPeaker 4-Mic Aarray to perform 
speech recognition with Google Speech Service

"""

from curt.command import CURTCommands
import time
import os
import json

# Modify these to your own workers
# Format is "<host_name>/<module_type>/<service_name>/<worker_name>"
RESPEAKER_WORKER = "charlie/voice/voice_input_service/respeaker_input"
VOICE_PROCESSING_WORKER = "charlie/voice/speech_to_text_service/online_voice_processing"

CURTCommands.initialize()

respeaker_worker = CURTCommands.get_worker(RESPEAKER_WORKER)
config_handler = CURTCommands.config_worker(respeaker_worker, {"audio_in_index": 3})
success = CURTCommands.get_result(config_handler)["dataValue"]["data"]

voice_processing_worker = CURTCommands.get_worker(VOICE_PROCESSING_WORKER)

curt_path = os.getenv("CURT_PATH")
with open(curt_path + "models/modules/voice/account.json") as f:
    account_info = json.load(f)
config_handler = CURTCommands.config_worker(
    voice_processing_worker,
    {
        "account_crediential": account_info,
        "language": "en-UK",
        "sample_rate": 16000,
        "channel_count": 4,
    },
)
success = CURTCommands.get_result(config_handler)["dataValue"]["data"]

count = 0

while True:
    count += 1

    voice_handler = CURTCommands.request(respeaker_worker, params=["get"])

    print("Start speech now")

    voice_processing_handler = CURTCommands.request(
        voice_processing_worker, params=[voice_handler]
    )

    speech_result = CURTCommands.get_result(voice_processing_handler)

    if count > 15:
        voice_handler = CURTCommands.request(respeaker_worker, params=["release"])

    print(speech_result)

    if count > 15:
        break
