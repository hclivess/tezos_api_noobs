import json
from datetime import datetime
import requests
import datetime
import dateutil
import time

# origination

decimals = 1000000000000000000
time_now = time.time()

contract = "KT1PxkrCckgh5fA5v2cZEE2bX5q2RV1rv8dj"
origination = 1734719
level = 1735011

url = f"https://api.tzkt.io/v1/operations/transactions?sender={contract}&entrypoint=burn&status=applied&level={level}"
print(url)

operations = json.loads(requests.get(url).text)

for_output = []

for operation in operations:
    value_readable = int(operation["parameter"]["value"]["value"]) / decimals

    print(f'{operation["initiator"]["address"]} applied '
          f'{operation["parameter"]["entrypoint"]} of '
          f'{operation["parameter"]["value"]["value"]}'
          f', which is {value_readable}')

    if value_readable >= 10000:
        for_output.append(operation)
        print("will be saved to file")

with open("output.json", "w") as outfile:
    outfile.write(json.dumps(for_output))
    print("file saved")
