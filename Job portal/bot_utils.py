import pickle
import numpy as np
import mysql.connector
import pandas as pd
from datetime import datetime
import uuid

with open('clickstream_rf_model.pkl', 'rb') as f:
    model, label_encoder = pickle.load(f)

def get_user_click_sequence(user_id):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='manager',
        database='clickhire'
    )
    query = f"SELECT page_visited FROM clickstream WHERE user_id = {user_id} ORDER BY timestamp"
    df = pd.read_sql(query, conn)
    conn.close()
    return df['page_visited'].tolist()

def pad_sequence(seq, maxlen=10, pad_value='PAD'):
    return seq[:maxlen] + [pad_value] * (maxlen - len(seq))

def detect_bot(user_id, ip_address):
    sequence = get_user_click_sequence(user_id)

    if not sequence:
        action = "No click activity"
    else:
        padded = pad_sequence(sequence)
        encoded = label_encoder.transform([s if s in label_encoder.classes_ else 'PAD' for s in padded])
        X = np.array(encoded).reshape(1, -1)
        prediction = model.predict(X)[0]
        action = "Flagged as Bot" if prediction == 1 else "Activity Normal"

    bot_id = f"BOT-{str(uuid.uuid4())[:8].upper()}"

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='manager',
        database='clickhire'
    )
    cursor = conn.cursor()
    insert_query = """
        INSERT INTO bots_detected (bot_id, ip_address, detected_on, action)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(insert_query, (bot_id, ip_address, datetime.now(), action))
    conn.commit()
    conn.close()

    return action