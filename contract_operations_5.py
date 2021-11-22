import json
import requests
import time

def fetch_url(url):
    while True:
        try:
            fetched = json.loads(requests.get(url).text)
            return fetched
        except Exception as e:
            print(f"{url} unreachable due to {e}, retrying")

def last_block():
    url = "https://api.tzkt.io/v1/head"
    result = fetch_url(url)
    return result["level"]


def load_previous():
    try:
        with open("database.json", "r") as infile:
            previous = json.loads(infile.read())
    except Exception as e:
        previous = {}
    return previous


def save_data(data):
    with open("database.json", "w") as outfile:
        outfile.write(json.dumps(data))
        print("file saved")


decimals = 1000000000000000000

contract = "KT1PxkrCckgh5fA5v2cZEE2bX5q2RV1rv8dj"
origination = 1734719
# level = 1735011

previous_data = load_previous()

try:
    start = previous_data["stats"]["last_block"]
except Exception as e:
    start = origination

end = last_block()

for block in range(start, end + 1):
    print(f"Processing block {block}")

    for_output = {'last_block': block}

    url = f"https://api.tzkt.io/v1/operations/transactions?sender={contract}" \
          f"&entrypoint.in=burn,mint" \
          f"&status=applied" \
          f"&level={block}"

    operations = fetch_url(url)

    for operation in operations:
        print(f"Processing operation {operation}")
        value_readable = int(operation["parameter"]["value"]["value"]) / decimals

        print(f'{operation["initiator"]["address"]} applied '
              f'{operation["parameter"]["entrypoint"]} of '
              f'{operation["parameter"]["value"]["value"]}'
              f', which is {value_readable}')

        for_output[operation["hash"]] = operation

    previous_data = load_previous()
    merged = {**previous_data, **for_output}

    if operations:
        save_data(merged)
