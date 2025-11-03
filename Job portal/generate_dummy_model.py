import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Fake page sequences (simulate real vs bot clicks)
X_raw = [
    ['welcome', 'login', 'content', 'job_detail', 'apply', 'logout'],
    ['welcome', 'register', 'login', 'content', 'company_detail', 'logout'],
    ['welcome', 'login', 'logout'],  # Bot-like
    ['login', 'job_detail', 'job_detail', 'job_detail', 'logout'],  # Bot-like
    ['register', 'login', 'content', 'job_detail', 'apply', 'logout'],
]

y = [0, 0, 1, 1, 0]  # 0 = Human, 1 = Bot

# Flatten and encode all unique pages
le = LabelEncoder()
flat_pages = [page for seq in X_raw for page in seq]
le.fit(flat_pages)

# Encode sequences
def encode_sequence(seq, maxlen=10):
    seq = seq[:maxlen] + ['PAD'] * (maxlen - len(seq))
    return le.transform([s if s in le.classes_ else 'PAD' for s in seq])

# Add 'PAD' label to encoder
le_classes = list(le.classes_)
if 'PAD' not in le_classes:
    le_classes.append('PAD')
    le.classes_ = np.array(le_classes)

X = np.array([encode_sequence(seq) for seq in X_raw])
y = np.array(y)

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save both model and label encoder
with open('clickstream_rf_model.pkl', 'wb') as f:
    pickle.dump((model, le), f)

print("✅ Dummy model and encoder saved to clickstream_rf_model.pkl")