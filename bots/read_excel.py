import pandas as pd

GIFT_FILE = './data/gifts_info.csv'

data = pd.read_csv(GIFT_FILE)

print(str(data))