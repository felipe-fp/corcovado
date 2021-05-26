import numpy as np
import pandas as pd
from scipy.stats import stats
from scipy.stats.stats import _threshold_mgc_map
from statsmodels.tsa.stattools import adfuller 

class Stats:

    # If you change anything here, please run test_stats 
    # to verify everything is ok.

    def __init__(self):
        pass
    
    # Differenciate a time series one time
    def differentiate(self, ts):
        # Differentiate with delta equal to 1
        ts_diff = ts - ts.shift(1) 
        # Delete first line nan
        ts_diff.dropna(inplace = True) 

        return ts_diff

    # Return p-value of the stationarity
    def unit_root_test(self, ts):
        return adfuller(ts.values)[1]

    def add_to_df(self, df, ts, name):
        # Add differentiated time series to final dataframe
        if df.shape[0] == 0:
            df = pd.DataFrame(ts)
            df.columns = [name]

        else:
            df_to_add = pd.DataFrame(ts)
            df_to_add.columns = [name]
            # Inner join
            df = df.join(df_to_add, how='inner')

        return df
    
    def get_iterations(self, ts, MAX_ITER = 4, THRESHOLD = 0.1):
        # Check max iteractions constraint
        iter = 0
        while iter < MAX_ITER and self.unit_root_test(ts) > THRESHOLD:
            ts = self.differentiate(ts)
            iter += 1
        
        return iter

    # UI to get data stationary
    def get_stationary(self, df, auto = True, log_flag = False, same = False, verbose = True):
        
        new_df = pd.DataFrame()
        iters = {}

        if log_flag:
            df = np.log(df)

        if auto:

            for column in df.columns:
                
                ts = df[column]
                # Add number of differentiation on iters dict
                iters[column] = self.get_iterations(ts)
            
            if same:

                MAX = max(iters.values())

                for column in df.columns:
                
                    ts = df[column]

                    # Differentiate MAX - iter timer:
                    for i in range(MAX):
                        ts = self.differentiate(ts)
                    
                    new_df = self.add_to_df(new_df, ts, column)
                    
                    if verbose:
                        print('[STATS] You have diffentiated',column, MAX,'times.')
                        print('[STATS] Final p-value is', self.unit_root_test(ts),'.')
            
            else:

                for column in df.columns:
                
                    ts = df[column]

                    # Differentiate MAX - iter timer:
                    for i in range(iters[column]):
                        ts = self.differentiate(ts)
                    
                    new_df = self.add_to_df(new_df, ts, column)
                    
                    if verbose:
                        print('[STATS] You have diffentiated',column, iters[column],'times.')
                        print('[STATS] Final p-value is', self.unit_root_test(ts),'.')

        return new_df

        


        
        




