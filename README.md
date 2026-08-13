# Intelligent Food Business Management System

A beginner-friendly AI project for the Artificial Intelligence Lab. The system combines **Machine Learning** and **Natural Language Processing (NLP)** to help a food business understand sales, inventory, food waste and customer feedback.

The project follows the submitted outline: Sales Prediction, Inventory Prediction, Food Waste Prediction, Smart Menu Recommendation, Customer Review Sentiment Analysis, AI Chatbot and an Admin Dashboard. The outline also identifies Python, Scikit-learn, Pandas, NumPy and NLTK as project technologies. The implementation uses a simple Streamlit interface and SQLite database instead of adding unnecessary backend complexity.

## 1. Project Overview

Food businesses can have problems with demand estimation, inventory planning, food waste and manual review analysis. This application turns historical order data into simple AI-assisted decisions.

Main workflow:

```text
CSV Dataset
    ↓
Data Cleaning
    ↓
Feature Preparation
    ↓
Machine Learning + NLP
    ↓
Predictions / Recommendations
    ↓
SQLite + Streamlit Dashboard
```

## 2. Features

- Admin dashboard
- Sales prediction
- Inventory usage prediction
- Food waste prediction
- Smart menu recommendation
- Customer review sentiment analysis
- Simple AI chatbot
- SQLite data storage
- Searchable order data
- CSV report download
- Model evaluation metrics
- User-friendly Streamlit interface
- Input validation and error handling

## 3. Technologies Used

- Python 3.14.2
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- SQLite (Python standard library)
- NLTK is listed in the original project outline, but this simple implementation does not require downloading NLTK corpora. TF-IDF from Scikit-learn is used for the sentiment module to keep installation simple.

The selected package versions are intentionally modern because the project is requested for Python 3.14.2.

## 4. Project Architecture

### UI layer
`app.py`

Controls the Streamlit pages and collects user input.

### Database layer
`database.py`

Creates SQLite tables, imports the provided dataset on first run, and stores new reviews.

### Data layer
`utils/data_utils.py`

Checks required columns, removes duplicates, converts dates and numeric fields, and handles missing values.

### ML layer
`utils/ml_models.py`

Contains three Random Forest regression models:

1. Sales Prediction
2. Inventory Prediction
3. Food Waste Prediction

### NLP layer
`utils/nlp_models.py`

Uses:

```text
Customer Review
      ↓
TF-IDF Vectorizer
      ↓
Multinomial Naive Bayes
      ↓
Positive / Neutral / Negative
```

### Recommendation layer
`utils/recommendation.py`

Ranks menu items using sales quantity and average rating.

### Chatbot layer
`utils/chatbot.py`

Uses simple keyword/rule matching. It does not need an external API or API key.

## 5. Folder Structure

```text
Intelligent_Food_Business_Management_System/
│
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── restaurant_business_dataset.csv
│
├── models/
│   └── (generated model files can be stored here later)
│
├── utils/
│   ├── __init__.py
│   ├── data_utils.py
│   ├── ml_models.py
│   ├── nlp_models.py
│   ├── recommendation.py
│   ├── chatbot.py
│   └── metrics.py
│
└── tests/
    └── test_project.py
```

`food_business.db` is created automatically after the first application start and is ignored by Git.

## 6. Installation

### Step 1: Install Python

Install Python 3.14.2 and make sure the Python launcher is available.

Check:

```powershell
py --version
```

Expected:

```text
Python 3.14.2
```

### Step 2: Open the project folder

```powershell
cd "C:\path\to\Intelligent_Food_Business_Management_System"
```

Use your actual Windows project path.

### Step 3: Create a virtual environment

```powershell
py -3.14 -m venv .venv
```

### Step 4: Activate it

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Command Prompt:

```cmd
.venv\Scripts\activate
```

If PowerShell blocks activation, you can run the project using:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

### Step 5: Upgrade pip

```powershell
python -m pip install --upgrade pip
```

### Step 6: Install dependencies

```powershell
pip install -r requirements.txt
```

## 7. Run the Project

```powershell
streamlit run app.py
```

Streamlit will show a local address in the terminal. Open that address in your browser.

## 8. How the Database Works

On first launch:

1. SQLite database is created.
2. `orders` table is created.
3. The CSV dataset is inserted into the table.
4. `reviews` table is created.
5. New reviews entered from the UI are stored in SQLite.

No database server is required.

## 9. Dataset

The included dataset contains 5,000 food-business records with fields including:

- Order ID
- Order Date
- Day of Week
- Month
- Customer ID
- Menu Item
- Category
- Quantity Sold
- Unit Price
- Total Sales
- Inventory Stock
- Inventory Used
- Food Waste
- Customer Rating
- Review
- Sentiment
- Payment Method
- Branch

## 10. Machine Learning Component

### A. Sales Prediction

**Algorithm:** Random Forest Regression

**Input:**
- Menu Item
- Category
- Branch
- Day
- Month
- Expected Quantity Sold
- Unit Price

**Output:**
- Predicted sales amount

Why Random Forest?

- Works well with nonlinear relationships.
- Handles mixed feature types after encoding.
- Usually performs well on small/medium tabular datasets.
- Easy to explain in a viva.

### B. Inventory Prediction

**Algorithm:** Random Forest Regression

**Input:**
- Menu Item
- Category
- Branch
- Day
- Month
- Expected Quantity Sold
- Unit Price
- Current Inventory Stock

**Output:**
- Estimated inventory usage

### C. Food Waste Prediction

**Algorithm:** Random Forest Regression

**Input:**
- Menu Item
- Category
- Branch
- Day
- Month
- Expected Quantity Sold
- Unit Price
- Current Inventory Stock

**Output:**
- Estimated food waste

### Evaluation

The regression models use an 80/20 train-test split.

Metrics:

- MAE: Mean Absolute Error
- RMSE: Root Mean Squared Error
- R²: coefficient of determination

A lower MAE/RMSE is better. A higher R² is generally better.

## 11. NLP Sentiment Analysis

The dataset already contains a `Review` column and a `Sentiment` label.

The model is:

```text
Review
  ↓
TF-IDF
  ↓
Multinomial Naive Bayes
  ↓
Sentiment
```

**Input:** customer review text.

**Output:** Positive, Neutral or Negative.

Why Naive Bayes?

- Very simple.
- Fast for text classification.
- Works well with word-frequency based features.
- Easy to explain in a university viva.

Evaluation:

- Accuracy
- Precision
- Recall
- F1-score

## 12. Smart Menu Recommendation

This is intentionally a simple recommendation system rather than a complicated neural network.

For a selected branch/category, each menu item receives a score based on:

```text
Popularity score =
70% normalized quantity sold
+
30% normalized average customer rating
```

The highest scoring items are recommended.

This is easy to demonstrate:

> "Pizza has high sales and a good rating, so the system ranks Pizza highly."

## 13. AI Chatbot

The chatbot is a lightweight rule-based assistant.

Examples:

- "What is the most popular food?"
- "What are the total sales?"
- "How much food waste?"
- "What is the average rating?"
- "How can I check inventory?"

No API key is needed.

This keeps the project reliable and beginner-friendly.

## 14. Dashboard

The dashboard shows:

- Total orders
- Total sales
- Total food waste
- Average customer rating
- Monthly sales chart
- Top menu items
- Sentiment distribution
- Model performance

## 15. Testing

Run:

```powershell
pip install pytest
pytest
```

The tests check:

- Dataset cleaning
- ML prediction functions
- NLP prediction
- Basic output validity

If you want to keep dependencies minimal, you can also manually test the application by running:

```powershell
streamlit run app.py
```

## 16. Common Errors and Solutions

### Error: `python is not recognized`

Try:

```powershell
py --version
```

If that works, use `py` instead of `python`.

### Error: `No module named streamlit`

Activate the virtual environment and run:

```powershell
pip install -r requirements.txt
```

### Error: PowerShell cannot activate `.venv`

Use the direct executable:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

### Error: Dataset not found

Make sure this file exists:

```text
data/restaurant_business_dataset.csv
```

### Error: Port already in use

Run:

```powershell
streamlit run app.py --server.port 8502
```

### Error after changing the dataset

Delete:

```text
food_business.db
```

Then start the app again so SQLite can be rebuilt from the CSV.

## 17. Viva Questions and Answers

### Q1. What is the main purpose of this project?

To use Machine Learning and NLP to improve sales forecasting, inventory planning, food waste prediction, menu recommendation and customer review analysis.

### Q2. Why did you use Python?

Python has simple syntax and strong libraries for data analysis, machine learning and web applications.

### Q3. Why Random Forest?

Random Forest can model nonlinear relationships and works well for structured/tabular business data.

### Q4. Is Random Forest classification or regression here?

Regression is used because sales, inventory usage and food waste are numeric values.

### Q5. Why do you use Naive Bayes for sentiment analysis?

Naive Bayes is fast, simple and suitable for text classification after converting text into numerical TF-IDF features.

### Q6. What is TF-IDF?

TF-IDF converts text into numerical values by measuring how important words are in documents.

### Q7. What is the input of sentiment analysis?

A customer review.

### Q8. What is the output?

Positive, Neutral or Negative.

### Q9. What is the difference between training and testing data?

Training data teaches the model. Testing data checks how well the trained model works on unseen examples.

### Q10. What is MAE?

Mean Absolute Error is the average absolute difference between actual and predicted values.

### Q11. What is R²?

R² measures how much variation in the target is explained by the regression model.

### Q12. What is the recommendation system doing?

It ranks menu items using sales popularity and customer rating.

### Q13. Why SQLite?

SQLite is lightweight, built into Python and does not require a separate database server.

### Q14. Why Streamlit?

It allows a Python beginner to build a usable web interface without learning a full frontend framework.

### Q15. Does the chatbot use ChatGPT or an external API?

No. The included chatbot is a simple rule-based chatbot so the project does not need an API key or internet connection.

### Q16. What are the limitations?

The dataset is relatively small and synthetic/academic in nature. The prediction quality depends on the historical data. The chatbot is rule-based and the recommendation system is popularity-based.

### Q17. How can you improve the project later?

Possible future improvements include:

- More real-world data
- Time-series forecasting
- User login and roles
- Better recommendation algorithms
- More advanced NLP
- Real-time order integration
- Cloud deployment
- More detailed inventory management

## 18. Viva-Friendly One-Minute Explanation

> "Our project is an Intelligent Food Business Management System using Machine Learning and Natural Language Processing. We use historical food-business data to predict sales, inventory usage and food waste using Random Forest Regression. For customer reviews, we convert text into TF-IDF features and classify sentiment using Multinomial Naive Bayes. We also recommend popular menu items using sales and customer ratings. A simple chatbot answers common business questions. All modules are integrated into a Streamlit dashboard, and SQLite is used for local data storage. The goal is to support data-driven decisions, reduce food waste and improve customer satisfaction."

## 19. Important Academic Note

This implementation is intentionally simple. It demonstrates the AI concepts stated in the project outline without pretending that a small academic dataset is a production forecasting system.

For a university viva, focus on explaining:

```text
Data
→ Cleaning
→ Features
→ Model
→ Prediction
→ Evaluation
→ Dashboard
```
