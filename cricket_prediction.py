import matplotlib
matplotlib.use('TkAgg')

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, roc_curve
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
import os

match = pd.read_csv("matches.csv")
delivery = pd.read_csv("deliveries.csv")
#combining the total score of the first inning with the match data
total_score_df = delivery.groupby(["match_id", "inning"]).sum()["total_runs"].reset_index()
total_score_df = total_score_df[total_score_df["inning"] == 1]

match_df = match.merge(
    total_score_df[["match_id", "total_runs"]],
    left_on="id",
    right_on="match_id"
)

teams = [
    "Sunrisers Hyderabad", "Mumbai Indians", "Royal Challengers Bangalore",
    "Kolkata Knight Riders", "Kings XI Punjab", "Chennai Super Kings",
    "Rajasthan Royals", "Delhi Capitals"
]
# Replacing old team names with new ones to maintain consistency
match_df["team1"] = match_df["team1"].replace({
    "Delhi Daredevils": "Delhi Capitals",
    "Deccan Chargers": "Sunrisers Hyderabad"
})
match_df["team2"] = match_df["team2"].replace({
    "Delhi Daredevils": "Delhi Capitals",
    "Deccan Chargers": "Sunrisers Hyderabad"
})

match_df = match_df[
    match_df["team1"].isin(teams) &
    match_df["team2"].isin(teams) &
    (match_df["dl_applied"] == 0)
]

match_df = match_df[["match_id", "city", "winner", "total_runs"]]
delivery_df = match_df.merge(delivery, on="match_id")
#innings 2 for  predicting the outcome of the match when the chasing team is batting
delivery_df = delivery_df[delivery_df["inning"] == 2]

# Converting total_runs to numeric and handling non-numeric values
delivery_df["total_runs_y"] = pd.to_numeric(delivery_df["total_runs_y"], errors="coerce")
# Cumulative sum of runs scored by the chasing team in the second inning
delivery_df["current_score"] = delivery_df.groupby("match_id")["total_runs_y"].cumsum()

delivery_df["runs_left"] = delivery_df["total_runs_x"] - delivery_df["current_score"]
delivery_df["balls_left"] = 120 - (delivery_df["over"] * 6 + delivery_df["ball"])

# Handling player_dismissed column to calculate wickets left
delivery_df["player_dismissed"] = delivery_df["player_dismissed"].fillna("0")

# Converting player_dismissed to binary (0 for not dismissed, 1 for dismissed)
delivery_df["player_dismissed"] = delivery_df["player_dismissed"].apply(lambda x: 0 if x == "0" else 1).astype(int)

wickets = delivery_df.groupby("match_id")["player_dismissed"].cumsum().values

delivery_df["wickets"] = 10 - wickets



delivery_df["crr"] = (delivery_df["current_score"] * 6) / (120 - delivery_df["balls_left"])
delivery_df["rrr"] = (delivery_df["runs_left"] * 6) / delivery_df["balls_left"]

delivery_df["result"] = (delivery_df["batting_team"] == delivery_df["winner"]).astype(int)

final_df = delivery_df[
    ["batting_team", "bowling_team", "city",
     "runs_left", "balls_left", "wickets",
     "total_runs_x", "crr", "rrr", "result"]
]

# Removing rows with infinite values and ensuring no division by zero in rrr calculation
final_df = final_df.sample(frac=1).dropna()
final_df = final_df[final_df["balls_left"] != 0]


x = final_df.drop("result", axis=1)
y = final_df["result"]


x.replace([np.inf, -np.inf], np.nan, inplace=True)
x.dropna(inplace=True)
y = y[x.index]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

# ColumnTransformer to apply OneHotEncoder to categorical features and pass through numerical features
trf = ColumnTransformer([
    # OneHotEncoder with drop="first" to avoid dummy variable trap
    ("trf", OneHotEncoder(sparse_output=False, drop="first"),
     ["batting_team", "bowling_team", "city"])
], remainder="passthrough")

# Pipeline to combine the ColumnTransformer and RandomForestClassifier
pipe = Pipeline([
    ("step1", trf),
    ("step2", RandomForestClassifier(random_state=1))
])

pipe.fit(x_train, y_train)

model_path = os.path.join(os.path.dirname(__file__), "ipl_model.pkl")
pickle.dump(pipe, open(model_path, "wb"))

y_pred = pipe.predict(x_test)
y_pred_proba = pipe.predict_proba(x_test)[:, 1]

train_pred = pipe.predict(x_train)

train_acc = accuracy_score(y_train, train_pred)
test_acc = accuracy_score(y_test, y_pred)

precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc = roc_auc_score(y_test, y_pred_proba)

print("Train Accuracy:", train_acc)
print("Test Accuracy:", test_acc)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
print("ROC AUC:", roc)

cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:\n", cm)
print("\nClassification Report:\n", classification_report(y_test, y_pred))

plt.figure()
sns.heatmap(cm, annot=True, fmt='d')
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

plt.figure()
plt.bar(["Train Accuracy", "Test Accuracy"], [train_acc, test_acc])
plt.title("Accuracy Comparison")
plt.ylabel("Accuracy")
plt.show()

plt.figure()
plt.bar(["Precision", "Recall", "F1"], [precision, recall, f1])
plt.title("Model Metrics")
plt.ylabel("Score")
plt.show()

fpr, tpr, _ = roc_curve(y_test, y_pred_proba)

plt.figure()
plt.plot(fpr, tpr)
plt.plot([0, 1], [0, 1])
plt.title("ROC Curve")
plt.xlabel("FPR")
plt.ylabel("TPR")
plt.show()

ohe = pipe.named_steps['step1']
rf = pipe.named_steps['step2']

features = ohe.get_feature_names_out()
importances = rf.feature_importances_

plt.figure()
plt.barh(features[:10], importances[:10])
plt.title("Feature Importance")
plt.xlabel("Importance")
plt.show()