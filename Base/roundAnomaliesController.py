#biblioteki zew
import pandas as pd

def roundCo_ordinates(co_ordinates):
    rounded = co_ordinates.astype(float).round(5)
    return rounded
