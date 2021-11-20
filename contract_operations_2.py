import json
import requests

decimals = 1000000000000000000

contract = "KT1PxkrCckgh5fA5v2cZEE2bX5q2RV1rv8dj"
url = f"https://api.better-call.dev/v1/contract/mainnet/{contract}/operations"

result = json.loads(requests.get(url).text)
filter = ["buy", "sell"]

operations = result["operations"]


for_output = []

for operation in operations:
    if operation["entrypoint"] in filter:
        #print(operation)
        print(f'{operation["source"]} applied '
              f'{operation["entrypoint"]} of '
              f'{operation["parameters"][0]["children"][0]["value"]}')

        for_output.append(operation)
        print("will be saved to file")

with open("output.json", "w") as outfile:
    outfile.write(json.dumps(for_output))
    print("file saved")
