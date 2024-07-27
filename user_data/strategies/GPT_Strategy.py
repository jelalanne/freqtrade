from freqtrade.strategy import IStrategy
from pandas import DataFrame
import talib.abstract as ta

class GPT_Strategy(IStrategy):
    # ROI table
    minimal_roi = {
        "0": 0.356,
        "166": 0.218,
        "861": 0.074,
        "2164": 0
    }

    # Stoploss
    stoploss = -0.319

    # Trailing stop
    trailing_stop = True
    trailing_stop_positive = 0.099
    trailing_stop_positive_offset = 0.149
    trailing_only_offset_is_reached = True

    # Optimal timeframe for the strategy
    timeframe = '1h'

    # Run "populate_indicators" only once per pair
    process_only_new_candles = True

    # Don't use exit signals
    use_exit_signal = False

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # RSI
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        
        # Short EMA
        dataframe['ema_short'] = ta.EMA(dataframe, timeperiod=20)
        
        # Long EMA
        dataframe['ema_long'] = ta.EMA(dataframe, timeperiod=50)
        
        # Bollinger Bands
        bollinger = ta.BBANDS(dataframe, timeperiod=20, nbdevup=2.0, nbdevdn=2.0, matype=0)
        dataframe['bollinger_upper'] = bollinger['upperband']
        dataframe['bollinger_middle'] = bollinger['middleband']
        dataframe['bollinger_lower'] = bollinger['lowerband']
        
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi'] < 40) &  # RSI moins restrictif
                (dataframe['close'] < dataframe['bollinger_lower']) &  # Prix sous la bande inférieure de Bollinger
                (dataframe['ema_short'] > dataframe['ema_long'])  # EMA courte au-dessus de la EMA longue
            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi'] > 60) &  # RSI moins restrictif
                (dataframe['close'] > dataframe['bollinger_upper']) &  # Prix au-dessus de la bande supérieure de Bollinger
                (dataframe['ema_short'] < dataframe['ema_long'])  # EMA courte en dessous de la EMA longue
            ),
            'sell'] = 1
        return dataframe

    def custom_stoploss(self, pair: str, trade, current_time, current_rate, current_profit, **kwargs) -> float:
        if current_profit < -0.05:
            return 0.01  # 1% stoploss pour quitter le trade immédiatement
        return 1  # Pas de stoploss
