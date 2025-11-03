import pandas as pd
import numpy as np
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='manager',
    database='clickhire'
)

query = "SELECT user_id, page_visited, timestamp FROM clickstream ORDER BY user_id, timestamp"
df = pd.read_sql(query, conn)

print("Sample clickstream data:")
print(df.head())

user_sequences = df.groupby('user_id')['page_visited'].apply(list)
print("\nUser click sequences:")
print(user_sequences.head())

all_pages = sorted({page for seq in user_sequences for page in seq})
all_pages.append("<PAD>")
page2id = {p: i for i, p in enumerate(all_pages)}

SEQ_LEN = 10

def encode_sequence(seq, length=SEQ_LEN):
    seq = seq[-length:]
    pad_needed = length - len(seq)
    seq = ['<PAD>'] * pad_needed + seq
    return [page2id[p] for p in seq]

X = np.vstack(user_sequences.apply(encode_sequence).values)

print("\nEncoded feature matrix shape:", X.shape)
print("First row (user_id={}):".format(user_sequences.index[0]), X[0])

y = np.zeros(len(X), dtype=int)

np.save('X_clickstream.npy', X)
np.save('y_labels.npy', y)
print("\nSaved X_clickstream.npy and y_labels.npy")