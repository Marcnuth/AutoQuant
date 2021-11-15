from abc import ABC


class Broker(ABC):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def default(cls, kick_start, commission):
        return DefaultBroker(kick_start=kick_start, commission=commission)


class DefaultBroker(Broker):
    def __init__(self, kick_start: float, commission: float) -> None:
        super().__init__()
        self.kick_start = kick_start
        self.commission = commission
