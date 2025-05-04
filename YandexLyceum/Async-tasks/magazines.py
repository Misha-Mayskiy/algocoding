import asyncio
import sys


async def buy_one_gift(gift_name, choose_time):
    scaled_choose_time = choose_time / 100.0
    print(f"Buy {gift_name}")
    await asyncio.sleep(scaled_choose_time)
    print(f"Got {gift_name}")


async def handle_stop(stop_num, stop_duration, available_gifts):
    print(f"\nBuying gifts at {stop_num} stop")
    scaled_stop_duration = stop_duration / 100.0
    current_stop_time = 0.0
    tasks_at_this_stop = []
    gifts_to_remove = []
    available_gifts.sort(key=lambda g: g['total_time'], reverse=True)

    for gift in available_gifts:
        scaled_choose_time = gift['choose_time'] / 100.0

        if current_stop_time + scaled_choose_time <= scaled_stop_duration:
            task = asyncio.create_task(buy_one_gift(gift['name'], gift['choose_time']))
            tasks_at_this_stop.append(task)
            current_stop_time += scaled_choose_time
            gifts_to_remove.append(gift)
        else:
            pass

    for gift in gifts_to_remove:
        available_gifts.remove(gift)

    if tasks_at_this_stop:
        await asyncio.gather(*tasks_at_this_stop)

    remaining_time = scaled_stop_duration - current_stop_time
    if remaining_time > 0:
        await asyncio.sleep(remaining_time)
    print(f"Arrive from {stop_num} stop")


async def main():
    stops_data = []
    gifts_data = []
    while True:
        try:
            line = input()
            if not line.strip():
                break
            duration, travel = map(int, line.split())
            stops_data.append({'duration': duration, 'travel': travel})
        except EOFError:
            break
        except ValueError:
            print("Invalid input format. Please enter two integers separated by space.")
            continue

    while True:
        try:
            line = input()
            if not line.strip():
                break
            parts = line.split()
            if len(parts) != 3:
                print("Invalid input format. Please enter name, choose_time, pack_time.")
                continue
            name = parts[0]
            choose = int(parts[1])
            pack = int(parts[2])
            gifts_data.append({
                'name': name,
                'choose_time': choose,
                'pack_time': pack,
                'total_time': choose + pack
            })
        except EOFError:
            break
        except ValueError:
            print("Invalid input format for gift details.")
            continue

    if not stops_data or not gifts_data:
        print("Error: No stops or no gifts entered.")
        return

    remaining_gifts = gifts_data[:]
    stop_number = 0

    for stop_info in stops_data:
        stop_number += 1
        await handle_stop(stop_number, stop_info['duration'], remaining_gifts)

    if remaining_gifts:
        print("\nBuying gifts after arrival")
        final_tasks = [
            buy_one_gift(gift['name'], gift['choose_time'])
            for gift in remaining_gifts
        ]
        await asyncio.gather(*final_tasks)


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
