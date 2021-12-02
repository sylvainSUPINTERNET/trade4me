import logging
from numpy.core.fromnumeric import product
import pandas as pd
import numpy as np 

logging.basicConfig(level=logging.DEBUG)


class MemMarketFollow(object):

    """
        dict that store as follow 
        {
            "ETH-EUR": <df>  (df that contains array of price for buy and sell) idx 0 is sell prices and idx 1 is buy prices
        }
    """
    tracker_df = {}
    
    def __init__(self, coinToFollow:list) -> None:
        self.coinToFollow = coinToFollow


    """
        product_id : ETH-EUR / BTC-EUR ...
        The term "bid" refers to the highest price a market maker will pay to purchase the stock. The ask price, also known as the "offer" price, will almost always be higher than the bid price.    
        The bid and ask price matter to investors because they impact the price that investors pay to buy shares or the money they receive when selling them. If you want to buy a share, you have to pay the ask price. If you want to sell shares, you'll receive the bid price.
        e.g 'best_bid': '50509.88', 'best_ask': '50520.44', 'side': 'sell'
            'best_bid': '4057.47', 'best_ask': '4058.66', 'side': 'buy'
    """
    def add_price(self, product_id, best_bid, best_ask, cleanup_signal=False):
        logging.info("Distribute bid / ask ...")

        if cleanup_signal == True:
            logging.info(f"Cleanup memory DF for {product_id}")
            self.tracker_df.pop(product_id)
            logging.info(f"Memory data for {product_id} reset with success !")

        if product_id in self.tracker_df:
            logging.info(f"Append to DF {product_id}")
            new_df = pd.DataFrame([[best_bid, best_ask]], columns=[f"{product_id}@sell", f"{product_id}@buy"])
            self.tracker_df[product_id] = self.tracker_df[product_id].append(new_df, ignore_index=True)
            
            # Log full DF for each product_id tracked
            logging.info(self.tracker_df[product_id])
        else:
            logging.info(f"Init DF for {product_id}")
            pd.DataFrame([[best_bid, best_ask]], columns=[f"{product_id}@sell", f"{product_id}@buy"])
            self.tracker_df[f"{product_id}"] = pd.DataFrame([[best_bid, best_ask]], columns=[f"{product_id}@sell", f"{product_id}@buy"])
       
       
       
        # else:
        #     logging.info(f"Append new dataFrame for {product_id}")
        # if self.tracker_df.get(f"{product_id}") is None:
        #     logging.info(f"Init distribution for {product_id}")
        #     self.tracker_df[f"{product_id}"] = pd.DataFrame([best_bid, best_ask], columns=[f"{product_id}@sell", f"{product_id}@buy"])
        # else:
        #     print("Append new dataframe (ignoring index)")
        #     self.tracker_df[f"{product_id}"].append(pd.DataFrame([best_bid, best_ask], columns=[f"{product_id}@sell", f"{product_id}@buy"], ignore_index=True))

        # if cleanup_signal is True:
        #     self.tracker_df.pop(f"{product_id}")
        #     self.tracker_df[f"{product_id}"] = {}



        # if direction == "buy": 
        #     logging.info("Add price for buy side")
        #     # if product_id in self.tracker_df:
        #     #     logging.info(f"Update tracker {product_id}")
                 
        #     #      # Ici il faut garder en mémoire quand on a un buy en attendant un sell  et vis versa
        #     #      # sinon on le distribue pas
        #     #     #  if len(self.buy_waiting_for_distrib) == len(self.sell_waiting_for_distrib):
        #     #     #      new_df = df = pd.DataFrame([[1, 2]], columns=col)
        #     #     #         df2 = pd.DataFrame([[3, 4]], columns=col)
        #     #     #         df3 = pd.DataFrame([[3, 4]], columns=col)
        #     #     #         df = df.append([df2, df3], ignore_index=True)

        #     # else:
        #     #     logging.info(f"Add new tracker for {product_id}")
        #     #     df = pd.DataFrame([ [] ], columns=[f"{product_id}@sell", f"{product_id}@buy"])
        #     #     # numpy_data = np.array([[], []])
        #     #     # df = pd.DataFrame(data=numpy_data, index=[f"{product_id}@sell", f"{product_id}@buy"])
        #     #     # self.tracker_df[f"{product_id}"] = df
        #     # #df = self.tracker_df[f"{product_id}"]
            
        #     # # get price like this
        #     # # df.iloc[:1][0:len(df.iloc[:1].columns) - 1].values.tolist()[0]
        #     # # df.iloc[1:][0:len(df.iloc[:1].columns) - 1].values.tolist()[0]
        #     #  # sell   
        #     # # print(df.iloc[:1] )

        #     # # buy
        #     # # print(df.iloc[1:])
            

        # elif direction == "sell":
        #     logging.info("Add price for sell side")
        # else:
        #     logging.info(f"Direction not supported : {direction}")
