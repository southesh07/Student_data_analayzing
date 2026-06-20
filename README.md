#  Student Analytics Dashboard

An interactive web dashboard to analyse student performance data.  
Built as a **beginner learning project** using Python data science tools.

---

##  Tools & Libraries Used

| Library | Purpose |
|---|---|
| **Pandas** | Read CSV, clean data, group & filter |
| **NumPy** | Calculate mean, max, min, std deviation |
| **Matplotlib** | Draw bar charts, pie charts, histograms, scatter plots |
| **Seaborn** | Draw box plots and heatmaps |
| **Streamlit** | Build the interactive web dashboard |

---

##  Project Structure

```
project/
├── app.py                          ← Main dashboard code
├── students_pandas_100_records.csv ← Student dataset
├── requirements.txt                ← Python packages needed
├── README.md                       ← This file
└── screenshots/                    ← Add screenshots here
```

---

##  How to Run

### Step 1 – Install Python packages
Open a terminal in the project folder and run:
```bash
pip install -r requirements.txt
```

### Step 2 – Run the dashboard
```bash
streamlit run app.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

---

##  What the Dashboard Does

###  Mandatory Analysis (all covered)
- **Total Students** — shown in the KPI cards at the top
- **Average Marks** — calculated with `numpy.mean()`
- **Highest & Lowest Marks** — calculated with `numpy.max()` / `numpy.min()`
- **Department-wise Analysis** — grouped table + bar chart + box plot
- **Gender-wise Analysis** — bar chart comparing Male vs Female
- **Top 10 Students** — table sorted by highest marks
- **Pass/Fail Statistics** — count, percentage, and donut-style chart
- **Correlation Analysis** — heatmap and scatter plot with trend line

###  Visualizations (5+)
| # | Chart Type | What it shows |
|---|---|---|
| 1 | **Bar Chart** | Average marks by department |
| 2 | **Pie Chart** | Number of students per department |
| 3 | **Histogram** | Distribution of all student marks |
| 4 | **Scatter Plot** | Attendance vs Marks with trend line |
| 5 | **Bar Chart** | Gender-wise average marks |
| 6 | **Box Plot** | Marks spread per department (Seaborn) |
| 7 | **Heatmap** | Correlation between Age, Marks, Attendance |

###  Interactive Features
- **Sidebar Filters** — filter by Department, Gender, and Marks range
- **Dataset Preview tab** — see the full cleaned table + statistics
- **Search tab** — search for a student by name or ID
- **Pass/Fail filter** — show only passing or failing students

---

##  Data Cleaning Steps (in `load_and_clean_data()`)

1. Remove duplicate rows (same StudentID)
2. Fill missing **Age** with the median age
3. Fill missing **Marks** with the median marks
4. Fill missing **Attendance** with the median attendance
5. Fill missing **City** with `"Unknown"`
6. Add a **Pass/Fail** column (Pass if Marks ≥ 50)
7. Add a **Grade** column (A+, A, B, C, D, F)

---

##  Key Concepts You Learn

- `pd.read_csv()` — read data from a file
- `df.dropna()`, `df.fillna()` — handle missing values
- `df.groupby()` — group data by a category
- `np.mean()`, `np.std()`, `np.polyfit()` — NumPy math
- `plt.bar()`, `plt.hist()`, `plt.scatter()` — Matplotlib charts
- `sns.boxplot()`, `sns.heatmap()` — Seaborn charts
- `st.dataframe()`, `st.metric()`, `st.pyplot()` — Streamlit widgets
- `st.sidebar`, `st.tabs()`, `st.columns()` — Streamlit layout

---
