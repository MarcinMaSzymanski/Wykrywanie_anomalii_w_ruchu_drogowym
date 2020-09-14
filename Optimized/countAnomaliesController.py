#biblioteki zew
import pandas as pd

#pliki wew

def countAnomalies(co_ordinates):
    count = co_ordinates.groupby(co_ordinates.columns.tolist()).size().reset_index(). \
        rename(columns={0: 'count'})
    return count