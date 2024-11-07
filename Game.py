import os
from colorama import init, Fore, Style
import keyboard
from time import sleep
from random import randint

init(autoreset=True)

def clear(): #Очистка консоли
    os.system('cls')

def rand(): #Рандом
    f = True
    while f:
        num = randint(794257444, 794257445)
        num_to = randint(794257444, 794257445)
        if num != 123456789 and num_to != 123456789:
            f = False
    return str(num), str(num_to)

def output(mode = 0, lg = 'ru', num = 0, num_to = 0): #Вывод интерфейса
    global save_num

    clear()
    if save_num == 0:
        save_num = num
    if lg == 'ru':
        print(f'{Fore.BLUE + "Нужно получить" + Style.RESET_ALL} из числа {Fore.RED + str(save_num) + Style.RESET_ALL} в число {Fore.GREEN + str(num_to) + Style.RESET_ALL}\n Число: {num}')
        print(f'{Fore.CYAN + "Выбран режим:" + Style.RESET_ALL} {"+" if mode == 0 else "-"}')
        print(f'\nУправление:\n{Fore.LIGHTCYAN_EX} + - увеличить число\n - - уменьшить число\n R - правила\n Esc - выход{Style.RESET_ALL}')
        print(f'Пояснение:\n {Fore.LIGHTCYAN_EX}Сначало, выбираете режим, потом нажимаете на число на цифровом блоке (по индексу с 1-9){Style.RESET_ALL}')
    else:
        print(f'{Fore.BLUE + "You need to get" + Style.RESET_ALL} from number {Fore.RED + str(save_num) + Style.RESET_ALL} the number {Fore.GREEN + str(num_to) + Style.RESET_ALL}\n Number: {num}')
        print(f'{Fore.CYAN + "The mode is selected:" + Style.RESET_ALL} {"+" if mode == 0 else "-"}')
        print(f'\nControl:\n{Fore.LIGHTCYAN_EX} + - increase the number\n - - reduce the number\n R - rule\n Esc - exit{Style.RESET_ALL}')
        print(f'Explanation:\n {Fore.LIGHTCYAN_EX}First, select the mode, then click on the number on the digital block (according to the index from 1-9){Style.RESET_ALL}')

def game_math(index = 0, mode = 0): #Математика
    global Steps

    num_time = list(map(int, num.strip()))
    num_index = num_time[index] - 1
    if mode == 0:
        if num_time[index] + 1 == 10:
            num_time[index] = 0
        else:
            num_time[index] += 1
        
        if num_time[num_index] - 1 == -1:
            num_time[num_index] = 9
        else:
            num_time[num_index] -= 1
        res = ''
        [res := res + i for i in list(map(str, num_time))]
        Steps.append(res)
        return res
    else:
        if num_time[index] - 1 == -1:
            num_time[index] = 9
        else:
            num_time[index] -= 1
        
        if num_time[num_index] + 1 == 10:
            num_time[num_index] = 0
        else:
            num_time[num_index] += 1
        res = ''
        [res := res + i for i in list(map(str, num_time))]
        Steps.append(res)
        return res

def game_win(lg = 'ru'): #Победа + логи
    clear()
    log = ''
    for i in Steps:
        if i != num_to:
            log += i + ' -> '
        else:
            log += i
    if lg == 'ru':
        print(f'Ты выйграл!\n количество твоих ходов:{len(Steps)-1}')
        print('\nНажми Esc, чтобы выйти в меню')
        print('\nНажми Enter, чтобы сохранить логи')
    else:
        print(f'You win!\n your steps:{len(Steps)-1}')
        print('\nPress Esc to exit to the menu')
        print('\nPress Enter to save the log')

    while True:
        if keyboard.is_pressed("esc"):
            if lg == 'ru':
                mRU()
            else:
                mEN()
        if keyboard.is_pressed("enter"):
            my_log = open('log.txt', 'w+')
            my_log.write(log)
            my_log.close()

def game(lg = 'ru'): #Код игры
    global flag, num, num_to, save_num, Steps

    if flag:
        num, num_to = rand()
        flag = False
    mode = 0
    sleep(0.5)
    #num, num_to = '900000000', '800000001'
    Steps.append(num)
    output(mode, lg, num, num_to) 
    while True:
        if num == num_to:
            game_win(lg)
            break
        sleep(0.1)
        if keyboard.is_pressed("+"):
            mode = 0
            output(mode, lg, num, num_to)
        elif keyboard.is_pressed("-"):
            mode = 1
            output(mode, lg, num, num_to)
        elif keyboard.is_pressed("r"):
            rules(lg, 'g')
            break
        elif keyboard.is_pressed("esc"):
            flag = True
            save_num = 0
            if lg == 'ru':
                mRU()
                break
            else:
                mEN()
                break
        if keyboard.is_pressed("1"):
            num = game_math(0, mode)
            output(mode, lg, num, num_to)
        elif keyboard.is_pressed("2"):
            num = game_math(1, mode)
            output(mode, lg, num, num_to)
        elif keyboard.is_pressed("3"):
            num = game_math(2, mode)
            output(mode, lg, num, num_to)
        elif keyboard.is_pressed("4"):
            num = game_math(3, mode)
            output(mode, lg, num, num_to)
        elif keyboard.is_pressed("5"):
            num = game_math(4, mode)
            output(mode, lg, num, num_to)
        elif keyboard.is_pressed("6"):
            num = game_math(5, mode)
            output(mode, lg, num, num_to)
        elif keyboard.is_pressed("7"):
            num = game_math(6, mode)
            output(mode, lg, num, num_to)
        elif keyboard.is_pressed("8"):
            num = game_math(7, mode)
            output(mode, lg, num, num_to)
        elif keyboard.is_pressed("9"):
            num = game_math(8, mode)
            output(mode, lg, num, num_to)

def language(): #Выбор языка для игры
    clear()
    print(f'{Fore.LIGHTBLUE_EX}Нажми 1, чтобы выбрать Русский язык\n{Fore.LIGHTCYAN_EX}Press 2 to select English')
    while True:
        if keyboard.is_pressed("1"):
            main('ru')
            break
        elif keyboard.is_pressed("2"):
            main('en')
            break

def main(lg = 'ru'): #Переадресатор + аним
    clear()
    anim()
    if lg == 'ru':
        mRU()
    elif lg == 'en':
        mEN()

def mRU(): #Меню ру
    clear()
    score = 0
    mainImg = [
        f'{Fore.BLUE + " 1. Начать игру" + Style.RESET_ALL}\n 2. Правила\n 3. Выход',
        f' 1. Начать игру\n{Fore.BLUE + " 2. Правила" + Style.RESET_ALL}\n 3. Выход',
        f' 1. Начать игру\n 2. Правила\n{Fore.BLUE + " 3. Выход" + Style.RESET_ALL}'
    ]

    print(f'{Fore.RED}Добро пожаловать в игру "Hell in the console"!\n{Fore.LIGHTCYAN_EX}Выбери пункт меню:{Style.RESET_ALL}')
    print(mainImg[score])
    print(f'\nУправление: \n{Fore.LIGHTCYAN_EX}↑ or W - вверх\n↓ or S - вниз\nEnter - выбрать\n{Style.RESET_ALL}')
    while True:
        sleep(0.1)
        if keyboard.is_pressed("up") or keyboard.is_pressed("w"):
            clear()
            if score != 0:
                score -= 1
            print(f'{Fore.RED}Добро пожаловать в игру "Hell in the console"!\n{Fore.LIGHTCYAN_EX}Выбери пункт меню:{Style.RESET_ALL}')
            print(mainImg[score])
            print(f'\nУправление: \n{Fore.LIGHTCYAN_EX}↑ or W - вверх\n↓ or S - вниз\nEnter - выбрать\n{Style.RESET_ALL}')
        elif keyboard.is_pressed("down") or keyboard.is_pressed("s"):
            clear()
            if score != 2:
                score += 1
            print(f'{Fore.RED}Добро пожаловать в игру "Hell in the console"!\n{Fore.LIGHTCYAN_EX}Выбери пункт меню:{Style.RESET_ALL}')
            print(mainImg[score])
            print(f'\nУправление: \n{Fore.LIGHTCYAN_EX}↑ or W - вверх\n↓ or S - вниз\nEnter - выбрать\n{Style.RESET_ALL}')
        if keyboard.is_pressed("enter"):
            if score == 0:
                game('ru')
                break
            elif score == 1:
                rules('ru', 'm')
                break
            else:
                exit()

def mEN(): #Меню анг
    clear()
    score = 0
    mainImg = [
        f'{Fore.BLUE + " 1. Start game" + Style.RESET_ALL}\n 2. Rule\n 3. Exit',
        f' 1. Start game\n{Fore.BLUE + " 2. Rule" + Style.RESET_ALL}\n 3. Exit',
        f' 1. Start game\n 2. Rule\n{Fore.BLUE + " 3. Exit" + Style.RESET_ALL}'
    ]

    print(f'{Fore.RED}Welcome to the game "Hell in the console"!\n{Fore.LIGHTCYAN_EX}Select a menu item:{Style.RESET_ALL}')
    print(mainImg[score])
    print(f'\nControl: \n{Fore.LIGHTCYAN_EX}↑ or W - Up\n↓ or S - Down\nEnter - Select\n{Style.RESET_ALL}')
    while True:
        sleep(0.1)
        if keyboard.is_pressed("up") or keyboard.is_pressed("w"):
            clear()
            if score != 0:
                score -= 1
            print(f'{Fore.RED}Welcome to the game "Hell in the console"!\n{Fore.LIGHTCYAN_EX}Select a menu item:{Style.RESET_ALL}')
            print(mainImg[score])
            print(f'\nControl: \n{Fore.LIGHTCYAN_EX}↑ or W - Up\n↓ or S - Down\nEnter - Select\n{Style.RESET_ALL}')
        elif keyboard.is_pressed("down") or keyboard.is_pressed("s"):
            clear()
            if score != 2:
                score += 1
            print(f'{Fore.RED}Welcome to the game "Hell in the console"!\n{Fore.LIGHTCYAN_EX}Select a menu item:{Style.RESET_ALL}')
            print(mainImg[score])
            print(f'\nControl: \n{Fore.LIGHTCYAN_EX}↑ or W - Up\n↓ or S - Down\nEnter - Select\n{Style.RESET_ALL}')
        if keyboard.is_pressed("enter"):
            if score == 0:
                game('en')
                break
            elif score == 1:
                rules('en', 'm')
                break
            else:
                exit()

def rules(lg = 'ru', how = 'm'): #Правила
    clear()
    if lg == 'ru':
        print(Fore.BLUE + 'Итак, даны два девятизначных числа (начальное и конечное). Требуется превратить одно в другое, совершая нехитрые манипуляции с цифрами:')
        print(' 1. Можно прибавить к любой цифре в числе единицу (прибавление единицы к девяти даст ноль). При этом единица отнимается от цифры, стоящей на месте, обозначаемом той цифрой, к которой прибавляется единица.')
        print(' 2. Можно отнять от любой цифры в числе единицу (отнимание единицы от нуля даст девять). При этом единица прибавляется к цифре, стоящей на месте, обозначаемом той цифрой, от которой отнимается единица.')
        print(' 3. Прибавление единицы к нулю или отнимание единицы от нуля больше ничего в числе не меняет, потому что он не обозначает какое бы то ни было место в числе.')
        print(Fore.GREEN + '\nЧтобы выйти нажмите esc')
    else:
        print(Fore.BLUE + 'So, two nine-digit numbers are given (initial and final). It is required to turn one into another by performing simple manipulations with numbers:')
        print(' 1. You can add one to any digit in the number (adding one to nine will give zero). In this case, the unit is subtracted from the digit standing in the place indicated by the digit to which the unit is added.')
        print(' 2. You can subtract one from any digit in the number (subtracting one from zero will give nine). In this case, the unit is added to the digit standing in the place indicated by the digit from which the unit is subtracted.')
        print(' 3. Adding one to zero or subtracting one from zero does not change anything else in the number, because it does not designate any place in the number.')
        print(Fore.GREEN + '\nTo exit, press esc')
    while True:
        if keyboard.is_pressed("esc"):
            if how == 'm':
                if lg == 'ru':
                    mRU()
                    break
                else:
                    mEN()
                    break
            else:
                game(lg)
                break

def anim(): #Анимация загрузки
    frame = [
        '|         0          |',
        '|##       10         |',
        '|#########50         |',
        '|########100#########|'
    ]
    Name = [
        f'{Fore.RED}Hell in the console',
        f'{Fore.YELLOW}Hell in the console',
        f'{Fore.BLUE}Hell in the console',
        f'{Fore.GREEN}Hell in the console'
    ]
    for i in range(4):
        print(f'\n  {Name[i]}\n       Loading:\n{frame[i]}')
        sleep(1.5)
        clear()

Steps = [] #Шаги разделённые ->
flag = True
num, num_to, save_num = 0, 0, 0

language()