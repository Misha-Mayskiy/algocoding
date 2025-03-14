import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--barbie', type=int, default=50, help='Отношение к куклам (0-100)')
parser.add_argument('--cars', type=int, default=50, help='Отношение к машинам (0-100)')
parser.add_argument('--movie', choices=['melodrama', 'football', 'other'], default='other',
                    help='Любимая телевизионная программа')

args = parser.parse_args()

if args.barbie < 0 or args.barbie > 100:
    args.barbie = 50
if args.cars < 0 or args.cars > 100:
    args.cars = 50

if args.movie == 'melodrama':
    movie_value = 0
elif args.movie == 'football':
    movie_value = 100
else:
    movie_value = 50

boy = int((100 - args.barbie + args.cars + movie_value) / 3)
girl = 100 - boy

print(f"boy: {boy}")
print(f"girl: {girl}")
