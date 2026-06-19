


import numpy as np
import pandas as pd






def re_fkt(liste: list[int]) -> list[int]:

    if len(liste):
        element = liste.pop(-1)
        
        print(element)
        re_fkt(liste)
    else:
        return

re_fkt([1,2,3,4,5])