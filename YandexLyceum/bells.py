class Bell:
    def __init__(self, *args, **kwargs):
        self.args = list(args)
        self.kwargs = kwargs

    def print_info(self):
        if self.args or self.kwargs:
            kwargs = ', '.join([f'{k}: {v}' for k, v in sorted(self.kwargs.items())])
            args = ', '.join(self.args)
            print('; '.join(filter(None, [kwargs, args])))
        else:
            print('-')


class BigBell(Bell):
    a = 0

    def sound(self):
        print('ding' if not self.a else 'dong')
        self.a = 1 - self.a

    def info(self):
        return BigBell

    def info_about(self):
        return 'BigBell'


class LittleBell(Bell):
    def sound(self):
        print("ding")

    def info(self):
        return LittleBell

    def info_about(self):
        return 'LittleBell'


class BellTower:
    def __init__(self, *bells):
        self.bells = list(bells)

    def append(self, bell):
        self.bells.append(bell)

    def sound(self):
        for bell in self.bells:
            bell.sound()
        print('...')

    def print_info(self):
        for n, bell in enumerate(self.bells, 1):
            print(f'{n} {bell.info_about()}')
            bell.print_info()
        print('')


class SizedBellTower(BellTower):
    def __init__(self, *bells, size=10):
        self.size = size
        self.bells = list(bells)[-size:]

    def append(self, bell):
        if len(self.bells) == self.size:
            self.bells.pop(0)
        self.bells.append(bell)


class TypedBellTower(BellTower):
    def __init__(self, *bells, bell_type=LittleBell):
        self.bell_type = bell_type
        self.bells = [bell for bell in bells if isinstance(bell, bell_type)]

    def append(self, bell):
        if isinstance(bell, self.bell_type):
            self.bells.append(bell)
