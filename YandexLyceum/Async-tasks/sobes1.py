import asyncio
import time


async def perform_task(name, task_num, prep_time, defense_time, rest_time=0):
    scaled_prep_time = prep_time / 100.0
    scaled_defense_time = defense_time / 100.0
    scaled_rest_time = rest_time / 100.0

    print(f"{name} started the {task_num} task.")
    await asyncio.sleep(scaled_prep_time)

    print(f"{name} moved on to the defense of the {task_num} task.")
    await asyncio.sleep(scaled_defense_time)

    print(f"{name} completed the {task_num} task.")

    if rest_time > 0:
        print(f"{name} is resting.")
        await asyncio.sleep(scaled_rest_time)


async def run_interview(candidate_data):
    name, prep1, def1, prep2, def2 = candidate_data
    rest_period = 5
    await perform_task(name, 1, prep1, def1, rest_period)
    await perform_task(name, 2, prep2, def2, 0)


async def interviews(*candidates):
    tasks = [run_interview(candidate) for candidate in candidates]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    data = [('Ivan', 5, 2, 7, 2), ('John', 3, 4, 5, 1), ('Sophia', 4, 2, 5, 1)]
    t0 = time.time()
    asyncio.run(interviews(*data))
    print(time.time() - t0)
