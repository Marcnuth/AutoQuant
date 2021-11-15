from abc import ABC, abstractmethod
from autoquant.collector import Collector
import pandas as pd
from sklearn.linear_model import LogisticRegression as _LogisticRegression


class Model(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.data = None
        self.model = None

    def with_data(self, data: pd.DataFrame):
        self.data = data
        return self

    @abstractmethod
    def preprocess(self, data):
        pass

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def predict(self, data):
        pass


class LogisticRegression(Model):
    def __init__(self) -> None:
        super().__init__()
        self.model = _LogisticRegression(random_state=0)

    def train(self):
        df = self.preprocess(self.data)
        X, y = df.drop('y', axis=1), df['y']
        self.model.fit(X, y)
        return self

    def predict(self, data):
        return self.model.predict(data)
