import argparse
import asyncio
from itertools import zip_longest
import re

import aiohttp
import aiofiles
from motor.motor_asyncio import AsyncIOMotorClient
import nest_asyncio


# to separate 2 loops from each other (monodb connection + our main logic)
nest_asyncio.apply()
# TODO: add config file via environ
MONGO_URI = 'mongodb://localhost:27017'
APACHE_REGEX = r'^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+)\s?(\S+)?\s?(\S+)?" (\d{3}|-) (\d+|-)\s?"?([^"]*)"?\s?"?([^"]*)?"?$'  # noqa
REGEX_NAMES = (
    "ip", "ident", "auth", "timestamp", "method", "request", "httpversion",
    "status_code", "bytes_", "referrer", "extra",
)
IP_LOCATION_SERVICE = '<your_service>'

# TODO: make file with settings and default connections
mongo_loop = asyncio.new_event_loop()
asyncio.set_event_loop(mongo_loop,)
client = AsyncIOMotorClient(MONGO_URI, io_loop=mongo_loop)
db = client.get_database("_events")
collection = db.get_collection("logs")


async def handle_log(file_path):
    async with aiofiles.open(file_path, mode='r') as f:
        async for line in f:
            parsed_log = re.match(APACHE_REGEX, line).groups()
            dict_data = await _pii_serialization(parsed_log)
            location_data = await get_location(parsed_log[0])
            dict_data.update(location_data)
            mongo_loop.run_until_complete(write_logs(dict_data))


async def _pii_serialization(data):
    data_dict = dict((key, val) for key, val in zip_longest(REGEX_NAMES, data))
    data_dict['ip'] = re.sub(r"(?:\.\d+){2}$", '.*.*', data_dict['ip'])
    # TODO: convert timestamp into datetime type

    return data_dict


async def write_logs(result):
    await collection.insert_one(result)


async def get_location(ip):
    """
    MVP for retriaving ip location via third-party service
    """
    result_example = {
        "timezone": "America/Chicago",
        "latitude": 37.751,
        "lon": 97.822
    }
    return result_example
    """
    MVP example
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(IP_LOCATION_SERVICE, data={'ip': ip}) as resp:
            location_data = resp.json()

    return location_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        '--filepath',
        help='Full path or local path of logfile',
        required=True
    )
    args = parser.parse_args()
    asyncio.run(handle_log(args.filepath))
