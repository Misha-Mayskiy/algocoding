class Road:
    def __init__(self, name, limit):
        self.name, self.limit = name, limit

    def allowed(self, v):  # можно ли ехать по дороге
        return True

    def speed_for(self, v):
        return min(self.limit, v.max_speed)


class Highway(Road):  # дефолт
    pass


class CityRoad(Road):  # без грузовиков
    def allowed(self, v):
        return not isinstance(v, Truck)


class DirtRoad(Road):  # только внедорожный транспорт
    def allowed(self, v):
        return getattr(v, "offroad", False)


class Vehicle:
    def __init__(self, model, max_speed, offroad=False):
        self.model, self.max_speed, self.offroad = model, max_speed, offroad

    def drive(self, road, km):
        if not road.allowed(self):
            return f"{self.model}: нельзя на {road.name}"
        v = road.speed_for(self)
        t = km / v
        return f"{self.model} по {road.name}: {km} км за {t:.2f} ч (ср. {v} км/ч)"


class Car(Vehicle):
    def __init__(self, model): super().__init__(model, 180)


class Truck(Vehicle):
    def __init__(self, model): super().__init__(model, 90)


class Motorcycle(Vehicle):
    def __init__(self, model, offroad=False):
        super().__init__(model, 140 if not offroad else 120, offroad)


highway, city_road, dirt_road = Highway("М-4", 130), CityRoad("Проспект", 60), DirtRoad("Просёлок", 70)
golf_car, volvo_truck, toyota_motorcycle = Car("Golf"), Truck("Volvo"), Motorcycle("Toyota", offroad=True)

for r in (highway, city_road, dirt_road):
    for v in (golf_car, volvo_truck, toyota_motorcycle):
        print(v.drive(r, 10))
