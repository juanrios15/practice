import asyncio
import aiohttp
import time

start_time = time.time()


async def main():
    async with aiohttp.ClientSession() as session:
        for number in range(1,151):
            pokemon_url = f'https://pokeapi.co/api/v2/pokemon/{number}'
            async with session.get(pokemon_url) as resp:
                pokemon = await resp.json()
                print(pokemon['name'])
            
loop = asyncio.get_event_loop()
loop.run_until_complete(main())

print("--- %s seconds ---" % (time.time() - start_time))


# import requests
# import time

# start_time = time.time()

# for number in range(1, 151):
#     url = f'https://pokeapi.co/api/v2/pokemon/{number}'
#     resp = requests.get(url)
#     pokemon = resp.json()
#     print(pokemon['name'])

# print("--- %s seconds ---" % (time.time() - start_time))
