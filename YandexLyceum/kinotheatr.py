class Movie:
    def __init__(self, title, duration):
        self.title = title
        self.duration = duration


class Ticket:
    def __init__(self, session, seat):
        self.session = session
        self.seat = seat


class Session:
    def __init__(self, movie, hall, start_time):
        self.movie = movie
        self.hall = hall
        self.start_time = start_time
        self.tickets_sold = []

    def sell_ticket(self, seat):
        if seat in self.hall.seats and seat not in self.tickets_sold:
            ticket = Ticket(self, seat)
            self.tickets_sold.append(ticket)
            return ticket
        return None

    def is_seat_available(self, seat):
        return seat in self.hall.seats and seat not in self.tickets_sold


class Hall:
    def __init__(self, name, rows, seats_per_row):
        self.name = name
        self.seats = [(row, seat) for row in range(1, rows + 1) for seat in range(1, seats_per_row + 1)]
        self.sessions = []

    def add_session(self, session):
        self.sessions.append(session)


class Cinema:
    def __init__(self, name):
        self.name = name
        self.halls = []

    def add_hall(self, hall):
        self.halls.append(hall)

    def find_nearest_session(self, movie, current_time):
        available_sessions = []
        for hall in self.halls:
            for session in hall.sessions:
                if session.movie == movie and session.start_time > current_time and len(session.tickets_sold) < len(
                        hall.seats):
                    available_sessions.append(session)
        return available_sessions

    def get_hall_plan(self, session):
        plan = []
        for seat in session.hall.seats:
            if seat in session.tickets_sold:
                plan.append("X")  # Занято
            else:
                plan.append("O")  # Свободно
        return plan


# # Пример использования
# cinema = Cinema("Cinemax")
# hall1 = Hall("Hall 1", 5, 10)
# cinema.add_hall(hall1)
#
# movie1 = Movie("Inception", 148)
# session1 = Session(movie1, hall1, "2024-10-01 19:00")
# hall1.add_session(session1)
#
# # Продаем билет
# ticket = session1.sell_ticket((1, 1))
#
# # Проверяем наличие свободных мест
# print(session1.is_seat_available((1, 1)))  # False
# print(session1.is_seat_available((1, 2)))  # True
#
# # Находим ближайший сеанс
# current_time = "2024-10-01 18:00"
# nearest_sessions = cinema.find_nearest_session(movie1, current_time)
# print(nearest_sessions)
#
# # Получаем план зала
# hall_plan = cinema.get_hall_plan(session1)
# print(hall_plan)
