import json

from sensor import Sensor
from display import Display
from pathlib import Path
from datetime import datetime
import json

class CarPark:

    def __init__(self,
                 location,
                 capacity,
                 log_file='log.txt',
                 plates = None,
                 sensors = None,
                 displays = None):
        self.location = location
        self.capacity = capacity
        self.plates = plates or []
        self.sensors = sensors or []
        self.displays = displays or []

        self.log_file = Path(log_file)
        if not self.log_file.exists():
            self.log_file.touch()

    def to_json(self, file_name):
        with open(file_name, 'w') as file:
            json.dump({"location": self.location,
                       "capacity": self.capacity,
                       "log_file": str(self.log_file)}, file)

    @staticmethod
    def from_json(file_name):
        """Allows the creation of an instance of CarPark from a JSON.
        >>> car_park = CarPark.from_json("some_file.txt")"""
        with open(file_name, 'r') as file:
            conf = json.load(file)
        return CarPark(location=conf["location"],
                       capacity=(conf["capacity"]),
                       log_file=conf["log_file"])




    @property
    def available_bays(self):
        # car_park.available_bays
        return max(0, self.capacity - len(self.plates))
    def __str__(self):
        return f'Welcome to {self.location} car park'

    def register(self, component):
        """register a component to car park"""
        if not isinstance(component, (Sensor, Display)):
            raise TypeError("Invalid component type!")

        if isinstance(component, Sensor):
            self.sensors.append(component)
        elif isinstance(component, Display):
            self.displays.append(component)

    def _log_car(self, action, plate):
        with self.log_file.open(mode='a') as file:
            file.write(f'{plate} {action} on the {datetime.now().strftime("%d/%m/%Y %H:%M")}\n')

    def add_car(self, plate):
        self.plates.append(plate)
        self._log_car('entered', plate)

    def remove_car(self, plate):
        self.plates.remove(plate)
        self._log_car('exited', plate)

    def update_displays(self):
        for display in self.displays:
            display.update({"Bays": self.available_bays,
                            "Temperature": 42,}
                           )
            print(f"Updating: {display}")



