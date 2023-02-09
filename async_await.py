

import asyncio
from time import sleep



async def tori():
	
	print("tori")

async def say_after(delay, what):
	await asyncio.sleep(delay)
	print(what)

async def main():
	task1 = asyncio.create_task(say_after(5, "world"))
	task2 = asyncio.create_task(say_after(4, "hello"))
	task3 = asyncio.create_task(tori())
	await task1
	await task2

	await task3

asyncio.run(main())