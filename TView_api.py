# main
import numpy as np
import pandas as pd
import re
import random
import json
import time
import string
from typing import List
from datetime import datetime

# API calls
from websocket import create_connection

# util
from tqdm.notebook import tqdm

class TViewAPI():
    """
    Description:
        Session constants
    """
    WEBSOCKET = True
    CHART = False
    headers = json.dumps({
        "Origin": "https://data.tradingview.com",
        "user-agent": "<v.y2000@gmail.com> scraping for educational use"
        })
    skip_messages = ["series_loading", "series_completed", 
                     "quote_completed", "du"]
    def __init__(self):
        self.request_version = 1
        self.websocket_session = self.generate_sesssion(self.WEBSOCKET)
        self.chart_session = self.generate_sesssion(self.CHART)

    def generate_sesssion(self, session:bool) -> str:
        """
        Description:
            Get {session prefix}_{random string}
        params:
            session (bool)
                True: for websocket
                False: for chart
        returns:
            (str) web socket session
        """
        string_length = 12
        letters = string.ascii_lowercase
        random_string = "".join(
            random.choice(letters) for i in range(string_length)
        )
        prefix = "qs" if session else "cs"
        return f"{prefix}_{random_string}"

    def prepend_header(self, sentences: str)-> str:
        """
        Description:
            format data into websocket message:
        params:
            sentence
                (str) contructed message
        returns:
            (str) An added prefix message
        example:
            ~m~54~m~{"m":"set_auth_token","p":["unauthorized_user_token"]}
        """
        return f"~m~{len(sentences)}~m~{sentences}"

    def construct_message(self, function_name: str, parameters: List[str]) -> str:
        """
        params:
            function_name
                (str) Function to summit into websocket
            parameters:
                List[str]: list paramaters to input into the function
        returns:
            (str) a message as a JSON format join without space
        example:
            {"m":"set_auth_token","p":["unauthorized_user_token"]}
        """
        return json.dumps(
            {"m": function_name, "p": parameters}, separators=(",", ":")
        )

    def create_message(self, function_name: str, parameters: List[str]) -> str:
        """
        Description:
            Integration of a created message function
        params:
            function_name:
                (str) Function to summit into websocket
            parameters:
                List[str]: list paramaters to input into the function
        returns:
            (str) message as websocket message format
        example:
            ~m~54~m~{"m":"set_auth_token","p":["unauthorized_user_token"]}
        """
        output = self.prepend_header(self.construct_message(function_name, parameters))
        return self.prepend_header(self.construct_message(function_name, parameters))

    def send_message(self, func: str, args: List[str]) -> int:
        """
        Description:
            Send formatted message
        params:
            ws:
                (websocket._core.WebSocket) web socket sesssoin
            func:
                (str) Function to summit into websocket
            args:
                List[str]: list paramaters to input into the function
        """
        res = self.ws.send(self.create_message(func, args))
        return res
    
    def receive_response(self):
        qsd_dicts = []
        loading = True
        while loading:
            res = self.ws.recv()
            for r in res.split("~m~"):
                try:
                    r = json.loads(r)
                except json.JSONDecodeError:
                    continue
                if not isinstance(r, dict):
                    continue
                if "session_id" in r:
                    seassion_info = r
                    continue
                elif "m" in r:
                    message = r.get("m")
                    # Break the loop if qsd starts to repeat
                    if message == "qsd":
                        if r in qsd_dicts:
                            seassion_info, series_description, data = None, None, None
                            loading = False
                            break
                        else:
                            qsd_dicts.append(r) 
                    elif message in self.skip_messages:
                        continue
                    elif message == "symbol_resolved":
                        series_description = r['p'][2]
                    elif message == "timescale_update":
                        data = pd.DataFrame(r['p'][1]['sds_1']['s'])['v'].apply(pd.Series)
                        data.columns = ['date', 'open', 'high', 'low', 'close']
                        loading = False
                    elif (message == "symbol_error") or (message == "series_error"):
                        seassion_info, series_description, data = None, None, None
                        loading = False
                        break
                    else:
                        # Todo
                        print(message)
                        print(r)
                else:
                    # Todo
                    print(r.keys())
                    print(r)
        return seassion_info, series_description, data

    def get_data(self, symbol: str, freq :str = "1M", nubmer_of_values: int = 1000):
        # Creating a websocket connection
        self.ws = create_connection("wss://data.tradingview.com/socket.io/websocket", headers=self.headers)

        # login and create seassions
        self.send_message("set_auth_token", ["unauthorized_user_token"])
        self.send_message("set_locale", ["en", "US"])
        self.send_message("chart_create_session", [self.chart_session, ""])
        self.send_message("quote_create_session", [self.websocket_session])

        # Request symbol data
        resolve_symbol = json.dumps({"symbol": symbol, "adjustment": "splits"})
        self.send_message("quote_add_symbols", [self.websocket_session, f"={resolve_symbol}"])
        self.send_message("resolve_symbol", [self.chart_session, "sds_sym_1", f"={resolve_symbol}"])
        self.send_message("create_series", [self.chart_session, "sds_1", f"s{self.request_version}", "sds_sym_1", freq, nubmer_of_values, ""])
        self.request_version+=1
        return self.receive_response()
    
    def get_series(self, symbols: List[str], freq :str = "1M", nubmer_of_values: int = 1000, sleep_time=5):
        dataset = []
        for symbol in tqdm(symbols, leave=True, desc = f'Retrieving data'):
            seassion_info, series_description, data = self.get_data(symbol, freq, nubmer_of_values)
            if type(data)!=type(None):
                data['symbol'] = symbol
                if 'country' in series_description:
                    data['country'] = series_description['country']
                if 'type' in series_description:
                    data['type'] = series_description['type']
                dataset.append(data)
            time.sleep(sleep_time)
        if len(dataset)!= 0:
            dataset = pd.concat(dataset).reset_index(drop=True)
            dataset['date'] = dataset['date'].apply(datetime.utcfromtimestamp)
        return dataset
