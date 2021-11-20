import json
import requests

decimals = 1000000000000000000

contract = "KT1PxkrCckgh5fA5v2cZEE2bX5q2RV1rv8dj"
url = f"https://api.better-call.dev/v1/contract/mainnet/{contract}/operations"
print(url)

result = json.loads(requests.get(url).text)
entry_filter = ["buy", "sell"]

operations = result["operations"]

for_output = []

for operation in operations:
    if operation["entrypoint"] in entry_filter:
        #print(operation)
        print(f'{operation["source"]} applied '
              f'{operation["entrypoint"]} of '
              f'{operation["parameters"][0]["children"][0]["value"]}'
              f', which is {int(operation["parameters"][0]["children"][0]["value"])/decimals}')

        for_output.append(operation)

with open("output.json", "w") as outfile:
    outfile.write(json.dumps(for_output))
