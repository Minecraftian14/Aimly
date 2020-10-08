import asyncio

from aiohttp import ClientSession
import json


async def met(dat):
    session = ClientSession()
    async with session.post(
            'https://api.jdoodle.com/v1/execute',
            json=dat
    ) as response:
        res = await response.json()
        print(res)
    await session.close()


with open('../../config.json') as conffile:
    config = json.load(conffile)

data = {
    'script': 'A = [1:10]; disp(mean(A))',
    'language': "octave",
    'versionIndex': "3",
    'clientId': config["jdoodle_cid"],
    'clientSecret': config["jdoodle_sec"]
}
asyncio.run(met(data))

# var request = require('request');
#
# var program = {
#     script : "",
#     language: "php",
#     versionIndex: "0",
#     clientId: "YourClientID",
#     clientSecret:"YourClientSecret"
# };
# request({
#     url: 'https://api.jdoodle.com/v1/execute',
#     method: "POST",
#     json: program
# },
# function (error, response, body) {
#     console.log('error:', error);
#     console.log('statusCode:', response && response.statusCode);
#     console.log('body:', body);
# });
