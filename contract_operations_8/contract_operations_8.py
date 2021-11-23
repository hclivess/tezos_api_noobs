import json
import requests
import threading
import tornado.ioloop
import tornado.web
import time

decimals = 1000000000000000000
contract = "KT1PxkrCckgh5fA5v2cZEE2bX5q2RV1rv8dj"
# origination = 1734719
origination = 1734757


# level = 1735011

def fetch_url(url):
    while True:
        try:
            fetched = json.loads(requests.get(url).text)
            return fetched
        except Exception as e:
            print(f"{url} unreachable due to {e}, retrying")


def get_last_block():
    url = "https://api.tzkt.io/v1/head"
    result = fetch_url(url)
    return result["level"]


def load_database():
    try:
        with open("database.json", "r") as infile:
            previous = json.loads(infile.read())
    except Exception as e:
        previous = get_clear_dict()
    return previous


def save_data(data):
    with open("database.json", "w") as outfile:
        outfile.write(json.dumps(data))
        print("file saved")


def merge_save(output_dict):
    print("Saving...")
    input_dict = load_database()

    merged_data = {**input_dict["data"], **output_dict["data"]}
    merged_stats = output_dict["stats"]

    merged = {"data": merged_data, "stats": merged_stats}

    print(f"Total of {len(merged_data)} data entries")
    save_data(merged)


def get_clear_dict(dict_in={}):
    dict_in.clear()
    dict_out = {"data": {},
                "stats": {}
                }
    return dict_out


def get_last_saved_block():
    previous_data = load_database()

    try:
        last_saved = previous_data["stats"]["last_block"]
    except Exception as e:
        last_saved = origination
    return last_saved


def run():
    start = get_last_saved_block()
    end = get_last_block()

    for block in range(start, end + 1):
        print(f"Processing block {block}")

        url = f"https://api.tzkt.io/v1/operations/transactions?sender={contract}" \
              f"&entrypoint.in=burn,mint" \
              f"&status=applied" \
              f"&level={block}"

        operations = fetch_url(url)

        for_output = get_clear_dict()

        for operation in operations:
            
            print(f"Processing operation {operation}")
            value_readable = int(operation["parameter"]["value"]["value"]) / decimals

            print(f'{operation["initiator"]["address"]} applied '
                  f'{operation["parameter"]["entrypoint"]} of '
                  f'{operation["parameter"]["value"]["value"]}'
                  f', which is {value_readable}')

            for_output["stats"]["last_block"] = operation["level"]
            for_output["data"][operation["hash"]] = {"initiator": operation["initiator"]["address"],
                                           "operation": operation["parameter"]["entrypoint"],
                                           "value": operation["parameter"]["value"]["value"],
                                           "level": operation["level"],
                                           "timestamp": operation["timestamp"],
                                           }
        if operations:
            merge_save(for_output)


class RawHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(load_database())


def make_app():
    return tornado.web.Application([
        (r"/raw", RawHandler),
        (r"/", ReadHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),
    ])


class ReadHandler(tornado.web.RequestHandler):
    def get(self):
        database = load_database()

        self.render("dashboard.html",
                    title="Mints and Burns readable API",
                    data=database["data"],
                    decimals=decimals)


class ThreadedClient(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                run()
                run_interval = 360
                print(f"Sleeping for {run_interval / 60} minutes")
                time.sleep(run_interval)
            except Exception as e:
                print(f"Error: {e}")
                raise


if __name__ == "__main__":
    background = ThreadedClient()
    background.start()
    print("Background process started")

    app = make_app()
    app.listen(9878)
    print("Main process starting")
    tornado.ioloop.IOLoop.current().start()
