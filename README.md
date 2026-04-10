# 🏏 IPL Match Winner Prediction Model (99.73% Accuracy)

## 🚀 Project Overview

This project is a **Machine Learning-based IPL Match Winner Prediction System** that predicts the probability of a team winning during a live match scenario.

The model takes match conditions such as **current score, overs, wickets, and teams** and predicts the **winning chances in real time**.

🔥 Achieved an impressive **99.73% accuracy**, making it a high-performance predictive model.

---

## 🧠 Problem Statement

Cricket is a dynamic game where match outcomes change ball-by-ball.
This project aims to:

* Predict match outcomes during live matches
* Analyze match situations using data
* Provide real-time win probability

---

## 📂 Dataset

* Source: IPL Ball-by-Ball Dataset
* Contains:

  * Match details
  * Ball-by-ball data
  * Runs scored
  * Wickets
  * Teams

---

## ⚙️ Features Used

* Batting Team
* Bowling Team
* City
* Current Score
* Runs Left
* Balls Left
* Wickets Left
* Current Run Rate (CRR)
* Required Run Rate (RRR)

---

## 🏗️ ML Pipeline

```python
Data → Preprocessing → Feature Engineering → Model Training → Prediction
```

---

## 🔧 Technologies & Tools Used

* **Python**
* **Pandas**
* **NumPy**
* **Scikit-learn**
* **Matplotlib**
* **Seaborn**
* **Jupyter Notebook**
* **Flask (for deployment)**

---

## 🧪 Data Preprocessing

* Merged match & delivery datasets
* Filtered second innings data
* Created new features:

  * `runs_left`
  * `balls_left`
  * `wickets_left`
  * `crr` (current run rate)
  * `rrr` (required run rate)
* Handled missing values
* One-hot encoding for categorical features

---

## 🤖 Model Used

* **Random Forest Classifier**
* Pipeline used for preprocessing + model training
* Hyperparameter tuning applied

---

## 📊 Model Performance

* ✅ Accuracy: **99.73%**
* 📉 Confusion Matrix used for evaluation
* 📈 Train Accuracy: ~100%
* 📈 Test Accuracy: ~99.68%

---

## 📈 Visualization

* Confusion Matrix
* Accuracy comparison
* Match win probability graphs

---

## 💡 Key Highlights

* Real-time prediction capability
* Feature engineering significantly improved performance
* High accuracy with minimal overfitting
* Clean ML pipeline implementation

---

## ▶️ How to Run

```bash
git clone https://github.com/your-username/ipl-win-predictor.git
cd ipl-win-predictor
pip install -r requirements.txt
python app.py
```

---

## 📌 Project Structure

```bash
├── data/
├── notebooks/
├── model/
├── app.py
├── pipe.pkl
├── requirements.txt
└── README.md
```

---

## 🌐 Deployment

* Model deployed using **Flask**
* Can be integrated with frontend for real-time predictions

---

## 🔮 Future Improvements

* Add deep learning models (LSTM for sequence prediction)
* Improve generalization across seasons
* Deploy on cloud (AWS / Render / Railway)
* Add live API integration

---

## 🤝 Contributing

Feel free to fork this repository and improve the model or UI.

---

## 📜 License

This project is open-source and available under the MIT License.

---

## 👨‍💻 Author

**Maverick** 🛫
Building high-performance ML systems and pushing limits.

---
