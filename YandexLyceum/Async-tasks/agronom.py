import asyncio


async def _fertilizers(plant):
    print(f'7 Application of fertilizers for {plant}')
    await asyncio.sleep(3 / 1000)
    print(f'7 Fertilizers for the {plant} have been introduced')


async def _treatment(plant):
    print(f'8 Treatment of {plant} from pests')
    await asyncio.sleep(5 / 1000)
    print(f'8 The {plant} is treated from pests')


async def _grow(plant, soak, germ, root):
    print(f'0 Beginning of sowing the {plant} plant')
    print(f'1 Soaking of the {plant} started')

    fert_task = asyncio.create_task(_fertilizers(plant))
    treat_task = asyncio.create_task(_treatment(plant))

    await asyncio.sleep(soak / 1000)
    print(f'2 Soaking of the {plant} is finished')

    print(f'3 Shelter of the {plant} is supplied')
    await asyncio.sleep(germ / 1000)

    print(f'4 Shelter of the {plant} is removed')
    print(f'5 The {plant} has been transplanted')
    await asyncio.sleep(root / 1000)

    print(f'6 The {plant} has taken root')

    await asyncio.gather(fert_task, treat_task)

    print(f'9 The seedlings of the {plant} are ready')


async def sowing(*data):
    tasks = [asyncio.create_task(_grow(p, s, g, r)) for p, s, g, r in data]
    await asyncio.gather(*tasks)


data = [('carrot', 7, 18, 2),
        ('cabbage', 2, 6, 10),
        ('onion', 5, 12, 7)]

asyncio.run(sowing(*data))
