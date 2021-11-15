from enum import Enum, auto


class _ACTION(Enum):
    BUY = 1
    HOLD = 0
    SELL = -1


class Action:
    def __init__(self) -> None:
        pass

    def calcuate(self, data):
        pass


class QuantileAction(Action):
    def __init__(self, lower_bound: float, higher_bound: float) -> None:
        super().__init__()
        assert 0 < lower_bound < 1, f'lower bound should be in (0, 1)'
        assert 0 < higher_bound < 1, f'higher bound should be in (0, 1)'
        assert lower_bound < higher_bound, f'lower bound shoule be smaller than higher bound'
        self._low = lower_bound
        self._high = higher_bound

    def _which_action(self, current_value, all_data):
        if current_value < all_data.quantile(self._low):
            return _ACTION.BUY.value
        elif current_value > all_data.quantile(self._high):
            return _ACTION.SELL.value
        else:
            return _ACTION.HOLD.value

    def calcuate(self, data):
        return data.map(lambda x: self._which_action(x, data))
