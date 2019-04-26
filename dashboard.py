from Robinhood.Robinhood import Robinhood
import pandas as pd
from collections import defaultdict

class InfoRetriever:
    INTERESTED_STOCK_ATTR = [
        'name', 'symbol', 'last_trade_price', 'quantity_held', 'dividend_yield', 'pe_ratio', 'pb_ratio', 
        'open', 'high', 'low', 'volume', 'float', 'high_52_weeks', 'low_52_weeks', 'description', 
        'sector', 'industry', 'market_cap'
    ]
    
    def __init__(self, trader):
        self.trader = trader
    
    def get_instruments_quant_owned(self):
        securities_owned = self.trader.securities_owned()['results']
        instruments_quant = []
        for sec in securities_owned:
            instrument_id, quantity = sec['instrument'].rsplit('/', 2)[-2], float(sec['quantity'])
            instruments_quant.append((instrument_id, quantity))
        return instruments_quant
    
    def get_stock_symbols_owned(self):
        instruments_quant = self.get_instruments_quant_owned()
        instrument_ids = []
        for instrument_id, quant in instruments_quant:
            instrument_ids.append(instrument_id)
        return self.get_stock_symbols(instrument_ids)
    
    def get_stock_symbols(self, instruments):
        symbols = []
        for instrument in instruments:
            symbols.append(self.get_stock_symbol(instrument))
        return symbols
    
    def get_stock_symbol(self, instrument_id):
        instrument_details = self.trader.instrument(instrument_id)
        return (instrument_details['symbol'], instrument_details['simple_name'])
    
    def quotes(self, symbols):
        return self.trader.quotes_data(symbols)
    
    def fundamentals(self, symbols):
        fundamentals = []
        for symbol in symbols:
            fundamentals.append(self.trader.fundamentals(symbol))
        return fundamentals
    
    def portfolio_holdings(self):
        instruments_quant = self.get_instruments_quant_owned()
        stocks_owned = self.get_stock_symbols_owned()
        stock_symbols = [symbol for symbol, name in stocks_owned]
        quotes = self.quotes(stock_symbols)
        fundamentals = self.fundamentals(stock_symbols)
        
        df_rows = []
        for (symbol, name), (instr, quant), quote, fundamental \
            in zip(stocks_owned, instruments_quant, quotes, fundamentals):
            merged_quote_fundamental_dict = quote.copy()
            merged_quote_fundamental_dict.update(fundamental)
            merged_quote_fundamental_dict['instrument_id'] = instr
            merged_quote_fundamental_dict['quantity_held'] = quant
            merged_quote_fundamental_dict['name'] = name
            
            df_row = {}
            for attribute in InfoRetriever.INTERESTED_STOCK_ATTR:
                df_row[attribute] = merged_quote_fundamental_dict[attribute]
            df_rows.append(df_row)
        
        return pd.DataFrame(df_rows)

def get_dashboard_data(user, password):
    my_trader = Robinhood.Robinhood()
    logged_in = my_trader.login(username=user, password=password)

    retriever = InfoRetriever(my_trader)
    portfolio_holdings = retriever.portfolio_holdings()

    total_port_value = 0
    sector_mkt_val = defaultdict(int)
    for _, row in portfolio_holdings.iterrows():
        total_port_value += float(row['last_trade_price']) * float(row['quantity_held'])
        sector_mkt_val[row['sector']] += float(row['last_trade_price']) * float(row['quantity_held'])

    sector_mkt_val_percent = {}
    for sector, val in sector_mkt_val.items():
        sector_mkt_val_percent[sector] = val / total_port_value * 100

    data = []
    for _, row in portfolio_holdings.iterrows():
        stock_info = {
            'name': row['name'],
            'symbol': row['symbol'],
            'market_cap': float(row['market_cap']),
            'pe_ratio': -6 if row['pe_ratio'] is None or float(row['pe_ratio']) < 0 else float(row['pe_ratio']),
            'dividend_yield': 0 if row['dividend_yield'] is None else float(row['dividend_yield']),
            'holding_val': float(row['last_trade_price']) * float(row['quantity_held']),
            'last_trade_price': float(row['last_trade_price']),
            'quantity_held': float(row['quantity_held']),
            'port_percent': float(row['last_trade_price']) * float(row['quantity_held']) / total_port_value * 100,
            'industry': row['industry'],
            'sector': row['sector'],
            'sector_port_percent': sector_mkt_val_percent[row['sector']],
            'description': row['description'],
        }
        data.append(stock_info)

    return data
