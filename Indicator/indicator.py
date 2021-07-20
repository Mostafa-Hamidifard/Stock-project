from abc import ABC

from abc import ABC, abstractmethod


class Indicator(ABC):
    @abstractmethod
    def __init__(self, raw_data):
        self.raw_data = raw_data

    @abstractmethod
    def plot(self):
        pass
