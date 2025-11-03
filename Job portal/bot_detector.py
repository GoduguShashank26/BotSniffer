import numpy as np
import pandas as pd
import joblib
import mysql.connector

model = joblib.load('clickstream_rf_model.pkl')

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='manager',
    database='clickhire'
)

query = """
SELECT user_id, page_visited, timestamp FROM clickstream
ORDER BY user_id, timestamp
"""
df = pd.read_sql(query, conn)

user_sequences = df.groupby('user_id')['page_visited'].apply(list)

unique_pages = ['content', 'job_1', 'job_2', 'job_detail_2', 'job_detail_3',
                'company_detail_amazon', 'company_detail_wipro']
page_to_id = {page: i+1 for i, page in enumerate(unique_pages)}

def encode_sequence(seq, max_len=10):
    encoded = [page_to_id.get(p, 0) for p in seq]
    if len(encoded) < max_len:
        encoded += [0] * (max_len - len(encoded))
    else:
        encoded = encoded[:max_len]
    return encoded

for user_id, sequence in user_sequences.items():
    encoded_seq = encode_sequence(sequence)
    X = np.array(encoded_seq).reshape(1, -1)
    prediction = model.predict(X)[0]
    label = "Bot" if prediction == 1 else "Human"
    print(f"User ID {user_id}: {label}")

conn.close()