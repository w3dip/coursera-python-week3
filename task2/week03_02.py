import os
import csv

def parse_float(value):
    try:
        return float(value)
    except ValueError:
        return 0.0

def parse_int(value):
    try:
        return int(value)
    except ValueError:
        return 0

class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = self.__parse_file_name(photo_file_name)
        self.carrying = parse_float(carrying)

    def __parse_file_name(self, photo_file_name):
        ext = self.__get_photo_file_ext_by_file_name(photo_file_name)
        return photo_file_name if ext in [".jpg", ".jpeg", ".png", ".gif"] else ""

    def __get_photo_file_ext_by_file_name(self, photo_file_name):
        return os.path.splitext(photo_file_name)[1] or ""

    def get_photo_file_ext(self):
        return self.__get_photo_file_ext_by_file_name(self.photo_file_name)

    def is_valid(self):
        return self.brand and self.photo_file_name and self.carrying



class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = parse_int(passenger_seats_count)
        self.car_type = "car"

    def is_valid(self):
        return super().is_valid() and self.passenger_seats_count


class Truck(CarBase):

    def __parse_body_whl(self, body_whl):
        if not body_whl:
            self.__set_default_dimensions()
        else:
            dimensions = body_whl.split('x')
            if len(dimensions) != 3:
                self.__set_default_dimensions()
            else:
                self.body_length = self.__parse_dimension(dimensions[0])
                self.body_width = self.__parse_dimension(dimensions[1])
                self.body_height = self.__parse_dimension(dimensions[2])

    def __set_default_dimensions(self):
        self.body_length = 0.0
        self.body_width = 0.0
        self.body_height = 0.0

    def __parse_dimension(self, dimension):
        try:
            return float(dimension)
        except ValueError:
            return 0.0

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.__parse_body_whl(body_whl)
        self.car_type = "truck"

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height

class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra
        self.car_type = "spec_machine"

    def is_valid(self):
        return super().is_valid() and self.extra


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            print(row)
            if len(row) == 0:
                continue
            car_type = row[0]
            if not car_type:
                continue
            brand = row[1]
            photo_file_name = row[3]
            body_whl = row[4]
            carrying = row[5]
            extra = row[6]
            if car_type == "car":
                passenger_seats_count = row[2]
                car_item = Car(brand, photo_file_name, carrying, passenger_seats_count)
                if car_item.is_valid():
                    car_list.append(car_item)
            if car_type == "truck":
                car_item = Truck(brand, photo_file_name, carrying, body_whl)
                if car_item.is_valid():
                    car_list.append(car_item)
            if car_type == "spec_machine":
                car_item = SpecMachine(brand, photo_file_name, carrying, extra)
                if car_item.is_valid():
                    car_list.append(car_item)
    return car_list

# car = Car('Bugatti Veyron', 'bugatti.png', '0.312', '2')
# print(car.car_type, car.brand, car.photo_file_name, car.carrying, car.passenger_seats_count, sep='\n')
#
# truck = Truck('Nissan', 'nissan.jpeg', '1.5', '3.92x2.09x1.87')
# print(truck.car_type, truck.brand, truck.photo_file_name, truck.body_length, truck.body_width, truck.body_height, sep='\n')
#
# spec_machine = SpecMachine('Komatsu-D355', 'd355.jpg', '93', 'pipelayer specs')
# print(spec_machine.car_type, spec_machine.brand, spec_machine.carrying, spec_machine.photo_file_name, spec_machine.extra, sep='\n')
#
# spec_machine.get_photo_file_ext()
#
# cars = get_car_list('coursera_week3_cars.csv')
# print(len(cars))
#
# for car in cars:
#     print(type(car))
#
# print(cars[0].passenger_seats_count)
#
# print(cars[1].get_body_volume())