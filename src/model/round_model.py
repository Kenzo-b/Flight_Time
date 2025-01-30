
class RoundModel:

    _teams_order = [['A','B'],['C','D']]

    def __init__(self):
        self._current_round = 1

    @property
    def current_round(self):
        return self._current_round

    @current_round.getter
    def current_round(self):
        return self._current_round

    @property
    def teams_order(self):
        return self._teams_order

    @teams_order.getter
    def teams_order(self):
        return self._teams_order if self.current_round % 2 == 1 else self._teams_order[::-1]

    def next_round(self):
        self._current_round += 1
