from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from pandas import DataFrame
import talib.abstract as ta

class EnhancedRSIStrategy(IStrategy):
    # ROI table
    minimal_roi = {
        "0": 0.1
    }

    # Stoploss
    stoploss = -0.10

    # Trailing stop
    trailing_stop = True
    trailing_stop_positive = 0.02
    trailing_stop_positive_offset = 0.04
    trailing_only_offset_is_reached = True

    # Optimal timeframe for the strategy
    timeframe = '1h'

    # Run "populate_indicators" only once per pair
    process_only_new_candles = True

    # Define the RSI periods
    rsi_period = IntParameter(7, 21, default=14, space='buy', optimize=True)
    rsi_period_sell = IntParameter(7, 21, default=14, space='sell', optimize=True)

    # Define the RSI thresholds
    rsi_buy = IntParameter(10, 40, default=30, space='buy', optimize=True)
    rsi_sell = IntParameter(60, 90, default=70, space='sell', optimize=True)

    # Define the SMA periods
    sma_short_period = IntParameter(5, 50, default=50, space='buy', optimize=True)
    sma_long_period = IntParameter(100, 300, default=200, space='buy', optimize=True)

    # Max drawdown protection
    max_drawdown = -0.2

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Calculate RSI
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=self.rsi_period.value)
        
        # Calculate short and long SMAs
        dataframe['sma_short'] = ta.SMA(dataframe, timeperiod=self.sma_short_period.value)
        dataframe['sma_long'] = ta.SMA(dataframe, timeperiod=self.sma_long_period.value)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi'] < self.rsi_buy.value) &  # RSI oversold
                (dataframe['sma_short'] > dataframe['sma_long'])  # Uptrend
            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi'] > self.rsi_sell.value)  # RSI overbought
            ),
            'sell'] = 1
        return dataframe

    def custom_stoploss(self, pair: str, trade, current_time, current_rate, current_profit, **kwargs) -> float:
        # Implement a custom stoploss logic here
        if current_profit < self.max_drawdown:
            return 0.01  # 1% stoploss to
