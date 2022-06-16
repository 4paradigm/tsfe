Initialization:
flow init --ip 127.0.0.1 --port 9380


1. upload data

flow data upload -c config.json


2. launch job

flow job submit -c config.json -d dsl.json


executable example in example.sh
