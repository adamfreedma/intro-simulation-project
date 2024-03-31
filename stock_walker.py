from typing import Tuple, List
from walker import Walker
import yfinance as yf # type: ignore[import]
import pandas as pd # type: ignore[import]
import random
import datetime
import math

class StockWalker(Walker):
    
    __DAY_COUNT = 1461
    __LIST_LENGTH = 1000
    
    def __init__(self, name: str, mass: float=1) -> None:
        super().__init__(name, mass)
        self.__current_stock_data = self.__choose_random_stock()
        self.__step = 1
        
        self._is_3d = False
        
    def __choose_random_stock(self) -> List[float]:
        try:
            tickers = pd.read_html(
        'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
            stock = yf.Ticker(random.choice(tickers['Symbol']))
            today = datetime.date.today()
            time_delta = datetime.timedelta(days=self.__DAY_COUNT)
            return stock.history(start=today-time_delta, end=today, interval='1d')['Close'].values.tolist()
        except Exception:
            return self.__choose_random_stock()
    
    def reset(self) -> None:
        self.__current_stock_data = self.__choose_random_stock()
        while len(self.__current_stock_data) < self.__LIST_LENGTH:
            print(len(self.__current_stock_data))
            self.__current_stock_data = self.__choose_random_stock()
        self.__step = 1
        self._location = (0, math.copysign(self.__SCALE, self.__current_stock_data[0]), 0)
        super().reset()

    def _generate_move_angle(self) -> Tuple[float, float]:
        stock_change = self.__current_stock_data[self.__step] - self.__current_stock_data[self.__step - 1]
        return (math.copysign(math.pi / 2, stock_change), 0)
            
    def _generate_move_radius(self) -> float:
        stock_change = abs(self.__current_stock_data[self.__step] - self.__current_stock_data[self.__step - 1])
        self.__step += 1
        return stock_change