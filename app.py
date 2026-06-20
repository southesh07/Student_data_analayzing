import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")


st.set_page_config(
    page_title="Student Analytics Dashboard",
    page_icon="🎓",
    layout="wide"
)


DATASET_FILE = "students_pandas_100_records.csv"

PASS_MARK = 50


@st.cache_data
def load_and_clean_data(file_path):
    df = pd.read_csv(file_path)

    print("Original shape:", df.shape)

    df = df.drop_duplicates(subset="StudentID", keep="first")

    df["Age"] = df["Age"].fillna(df["Age"].median())

    df["Marks"] = df["Marks"].fillna(df["Marks"].median())

    df["Attendance"] = df["Attendance"].fillna(df["Attendance"].median())

    df["City"] = df["City"].fillna("Unknown")

    df["Age"] = df["Age"].astype(int)

    df["Marks"] = df["Marks"].astype(float)
    df["Attendance"] = df["Attendance"].astype(float)

    df["Pass/Fail"] = df["Marks"].apply(lambda m: "Pass" if m >= PASS_MARK else "Fail")

    df["Grade"] = pd.cut(
        df["Marks"],
        bins=[0, 49, 59, 69, 79, 89, 100],
        labels=["F", "D", "C", "B", "A", "A+"]
    )

    print("Cleaned shape:", df.shape)
    return df


import os

if not os.path.exists(DATASET_FILE):
    st.error(f"❌ File '{DATASET_FILE}' not found! Put it in the same folder as app.py.")
    st.stop()

df_full = load_and_clean_data(DATASET_FILE)


st.sidebar.title("🎓 Student Dashboard")
st.sidebar.markdown("---")

all_departments = sorted(df_full["Department"].unique())

selected_departments = st.sidebar.multiselect(
    "Select Department(s)",
    options=all_departments,
    default=all_departments
)

all_genders = sorted(df_full["Gender"].unique())
selected_genders = st.sidebar.multiselect(
    "Select Gender(s)",
    options=all_genders,
    default=all_genders
)

min_mark = int(df_full["Marks"].min())
max_mark = int(df_full["Marks"].max())
marks_range = st.sidebar.slider(
    "Marks Range",
    min_value=min_mark,
    max_value=max_mark,
    value=(min_mark, max_mark)
)

st.sidebar.markdown("---")
st.sidebar.caption("Built with southesh")


df = df_full[
    df_full["Department"].isin(selected_departments) &
    df_full["Gender"].isin(selected_genders) &
    df_full["Marks"].between(marks_range[0], marks_range[1])
].copy()


st.title("🎓 Student Analytics Dashboard")
st.markdown("An interactive dashboard to explore student performance data.")
st.markdown("---")


st.subheader("📌 Quick Summary")

marks_array = df["Marks"].to_numpy()

total_students   = len(df)
average_marks    = np.mean(marks_array)
highest_marks    = np.max(marks_array)
lowest_marks     = np.min(marks_array)
std_deviation    = np.std(marks_array)
median_marks     = np.median(marks_array)

pass_count       = (df["Pass/Fail"] == "Pass").sum()
fail_count       = (df["Pass/Fail"] == "Fail").sum()
pass_percentage  = (pass_count / total_students * 100) if total_students > 0 else 0

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("👨‍🎓 Total Students",   total_students)
col2.metric("📊 Average Marks",      f"{average_marks:.1f}")
col3.metric("🏆 Highest Marks",      int(highest_marks))
col4.metric("⚠️ Lowest Marks",       int(lowest_marks))
col5.metric("✅ Pass Rate",          f"{pass_percentage:.1f}%")
col6.metric("📉 Std Deviation",      f"{std_deviation:.1f}")

st.markdown("---")


tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Dataset Preview",
    "📊 Charts",
    "🏫 Department Analysis",
    "🔍 Search Students",
    "📈 Correlation"
])
#page1

with tab1:
    st.subheader("📋 Dataset Preview")

    st.dataframe(df.reset_index(drop=True), use_container_width=True)

    st.markdown("**Dataset Info:**")

    info_col1, info_col2 = st.columns(2)

    with info_col1:
        st.write(f"- Total Rows: **{len(df)}**")
        st.write(f"- Total Columns: **{len(df.columns)}**")
        st.write(f"- Passed: **{pass_count}** students")
        st.write(f"- Failed: **{fail_count}** students")
        st.write(f"- Median Marks: **{median_marks:.1f}**")

    with info_col2:
        st.write("**Grades Breakdown:**")
        grade_counts = df["Grade"].value_counts().sort_index()
        for grade, count in grade_counts.items():
            st.write(f"  - Grade **{grade}**: {count} student(s)")

    st.subheader("📊 Descriptive Statistics (NumPy / Pandas)")
    st.markdown("This table shows count, mean, min, max, std, and percentiles for numeric columns.")

    st.dataframe(
        df[["Age", "Marks", "Attendance"]].describe().round(2),
        use_container_width=True
    )

#page2
with tab2:
    st.subheader("📊 Visualizations")

    chart_option = st.selectbox("Select a Chart", [
        "1️⃣ Bar Chart – Average Marks by Department",
        "2️⃣ Pie Chart – Students per Department",
        "3️⃣ Histogram – Distribution of Marks",
        "4️⃣ Scatter Plot – Attendance vs Marks",
        "5️⃣ Bar Chart – Gender-wise Average Marks"
    ])

    if chart_option == "1️⃣ Bar Chart – Average Marks by Department":
        dept_avg_marks = df.groupby("Department")["Marks"].mean().sort_values(ascending=False)

        fig1, ax1 = plt.subplots(figsize=(5, 2.5))

        ax1.bar(
            dept_avg_marks.index,
            dept_avg_marks.values,
            color=["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3"],
            edgecolor="black",
            width=0.5
        )

        ax1.set_title("Average Marks by Department", fontsize=14, fontweight="bold")
        ax1.set_xlabel("Department")
        ax1.set_ylabel("Average Marks")
        ax1.set_ylim(0, 100)
        ax1.grid(axis="y", linestyle="--", alpha=0.5)

        st.pyplot(fig1)
        plt.close(fig1)

    elif chart_option == "2️⃣ Pie Chart – Students per Department":
        dept_count = df["Department"].value_counts()

        fig2, ax2 = plt.subplots(figsize=(4, 3))

        ax2.pie(
            dept_count.values,
            labels=dept_count.index,
            autopct="%1.1f%%",
            startangle=140,
            colors=["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3"]
        )

        ax2.set_title("Department-wise Student Distribution", fontsize=14, fontweight="bold")
        st.pyplot(fig2)
        plt.close(fig2)

    elif chart_option == "3️⃣ Histogram – Distribution of Marks":
        st.markdown("A histogram shows how many students scored in each range.")

        fig3, ax3 = plt.subplots(figsize=(5, 2.5))

        ax3.hist(df["Marks"], bins=10, color="#4C72B0", edgecolor="black", alpha=0.8)

        ax3.axvline(average_marks, color="red", linestyle="--", linewidth=2,
                    label=f"Average: {average_marks:.1f}")

        ax3.axvline(PASS_MARK, color="green", linestyle=":", linewidth=2,
                    label=f"Pass Mark: {PASS_MARK}")

        ax3.set_title("Distribution of Student Marks", fontsize=14, fontweight="bold")
        ax3.set_xlabel("Marks")
        ax3.set_ylabel("Number of Students")
        ax3.legend()
        ax3.grid(axis="y", linestyle="--", alpha=0.5)

        st.pyplot(fig3)
        plt.close(fig3)

    elif chart_option == "4️⃣ Scatter Plot – Attendance vs Marks":
        st.markdown("Each dot is one student. We look for a pattern between attendance and marks.")

        fig4, ax4 = plt.subplots(figsize=(5, 2.5))

        ax4.scatter(
            df["Attendance"],
            df["Marks"],
            alpha=0.6,
            color="#4C72B0",
            edgecolors="white",
            linewidths=0.4,
            s=60
        )

        if len(df) > 1:
            coefficients = np.polyfit(df["Attendance"], df["Marks"], 1)
            trend_line = np.poly1d(coefficients)
            x_values = np.linspace(df["Attendance"].min(), df["Attendance"].max(), 100)
            ax4.plot(x_values, trend_line(x_values), color="red", linewidth=2,
                     linestyle="--", label="Trend Line")

        ax4.set_title("Attendance vs Marks", fontsize=14, fontweight="bold")
        ax4.set_xlabel("Attendance (%)")
        ax4.set_ylabel("Marks")
        ax4.legend()
        ax4.grid(True, linestyle="--", alpha=0.5)

        st.pyplot(fig4)
        plt.close(fig4)

    elif chart_option == "5️⃣ Bar Chart – Gender-wise Average Marks":
        gender_avg = df.groupby("Gender")["Marks"].mean()

        fig5, ax5 = plt.subplots(figsize=(4, 2.5))

        ax5.bar(
            gender_avg.index,
            gender_avg.values,
            color=["#DD8452", "#4C72B0"],
            edgecolor="black",
            width=0.4
        )

        for i, value in enumerate(gender_avg.values):
            ax5.text(i, value + 0.5, f"{value:.1f}", ha="center", fontsize=11, fontweight="bold")

        ax5.set_title("Average Marks by Gender", fontsize=14, fontweight="bold")
        ax5.set_xlabel("Gender")
        ax5.set_ylabel("Average Marks")
        ax5.set_ylim(0, 100)
        ax5.grid(axis="y", linestyle="--", alpha=0.5)

        st.pyplot(fig5)
        plt.close(fig5)
#page3

with tab3:
    st.subheader("🏫 Department-wise Analysis")

    dept_summary = df.groupby("Department").agg(
        Total_Students = ("StudentID", "count"),
        Average_Marks  = ("Marks", "mean"),
        Highest_Marks  = ("Marks", "max"),
        Lowest_Marks   = ("Marks", "min"),
        Avg_Attendance = ("Attendance", "mean"),
        Pass_Count     = ("Pass/Fail", lambda x: (x == "Pass").sum()),
        Fail_Count     = ("Pass/Fail", lambda x: (x == "Fail").sum())
    ).round(2).reset_index()

    dept_summary["Pass_Rate%"] = (
        dept_summary["Pass_Count"] / dept_summary["Total_Students"] * 100
    ).round(1)

    st.dataframe(dept_summary, use_container_width=True)

    st.subheader("🏆 Top 10 Students by Marks")

    top10 = df.nlargest(10, "Marks")[
        ["StudentID", "Name", "Department", "Gender", "Marks", "Attendance", "Grade", "Pass/Fail"]
    ].reset_index(drop=True)

    top10.index += 1
    st.dataframe(top10, use_container_width=True)

    st.subheader("📦 Box Plot – Marks spread per Department")
    st.markdown("A box plot shows the spread and median of marks for each department.")

    fig6, ax6 = plt.subplots(figsize=(10, 5))

    sns.boxplot(
        data=df,
        x="Department",
        y="Marks",
        palette="Set2",
        ax=ax6
    )

    ax6.axhline(PASS_MARK, color="red", linestyle="--", linewidth=1.5, label=f"Pass Mark ({PASS_MARK})")
    ax6.set_title("Marks Distribution by Department", fontsize=14, fontweight="bold")
    ax6.set_xlabel("Department")
    ax6.set_ylabel("Marks")
    ax6.legend()
    ax6.grid(axis="y", linestyle="--", alpha=0.5)

    st.pyplot(fig6)
    plt.close(fig6)

    st.subheader("✅ Pass vs Fail Count by Department")

    pf_by_dept = df.groupby(["Department", "Pass/Fail"]).size().unstack(fill_value=0)

    fig7, ax7 = plt.subplots(figsize=(9, 4))

    pf_by_dept.plot(
        kind="bar",
        ax=ax7,
        color={"Pass": "#55A868", "Fail": "#C44E52"},
        edgecolor="black",
        width=0.5
    )

    ax7.set_title("Pass vs Fail by Department", fontsize=14, fontweight="bold")
    ax7.set_xlabel("Department")
    ax7.set_ylabel("Number of Students")
    ax7.tick_params(axis="x", rotation=0)
    ax7.legend(title="Result")
    ax7.grid(axis="y", linestyle="--", alpha=0.5)

    st.pyplot(fig7)
    plt.close(fig7)


with tab4:
    st.subheader("🔍 Search & Filter Students")

    search_text = st.text_input(
        "Search by Name or Student ID",
        placeholder="e.g. Priya  or  1009"
    )

    filter_result = st.selectbox("Filter by Result", ["All", "Pass", "Fail"])

    result_df = df.copy()

    if search_text.strip() != "":
        query = search_text.strip().lower()

        name_match = result_df["Name"].str.lower().str.contains(query)
        id_match   = result_df["StudentID"].astype(str).str.contains(query)

        result_df = result_df[name_match | id_match]

    if filter_result != "All":
        result_df = result_df[result_df["Pass/Fail"] == filter_result]

    st.write(f"**Found {len(result_df)} student(s)**")

    st.dataframe(
        result_df[["StudentID", "Name", "Age", "City", "Department",
                   "Gender", "Marks", "Attendance", "Grade", "Pass/Fail"]]
        .reset_index(drop=True),
        use_container_width=True
    )


with tab5:
    st.subheader("📈 Correlation Analysis")
    st.markdown(
        "Correlation tells us if two numbers move together. "
        "A value close to **+1** means strong positive link. "
        "Close to **-1** means opposite relationship. "
        "Close to **0** means no relationship."
    )

    numeric_df = df[["Age", "Marks", "Attendance"]].dropna()

    correlation_matrix = numeric_df.corr()

    st.markdown("**Correlation Table:**")
    st.dataframe(correlation_matrix.round(3), use_container_width=True)

    st.markdown("### 🔥 Correlation Heatmap")
    st.markdown("Darker red = strong positive correlation. Darker blue = negative correlation.")

    fig8, ax8 = plt.subplots(figsize=(6, 4))

    sns.heatmap(
        correlation_matrix,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        linewidths=0.5,
        linecolor="white",
        ax=ax8
    )

    ax8.set_title("Correlation Between Age, Marks, and Attendance",
                  fontsize=13, fontweight="bold")

    st.pyplot(fig8)
    plt.close(fig8)

    st.markdown("### 💡 What does this tell us?")

    att_marks = correlation_matrix.loc["Attendance", "Marks"]
    age_marks = correlation_matrix.loc["Age", "Marks"]

    st.write(f"- **Attendance & Marks** correlation = `{att_marks:.3f}`")
    if att_marks > 0.3:
        st.success("✅ Students who attend more tend to score higher marks.")
    elif att_marks < -0.3:
        st.warning("⚠️ Surprisingly, higher attendance is linked to lower marks here.")
    else:
        st.info("ℹ️ There is a weak relationship between attendance and marks.")

    st.write(f"- **Age & Marks** correlation = `{age_marks:.3f}`")
    if abs(age_marks) < 0.2:
        st.info("ℹ️ Age does not seem to strongly affect marks in this dataset.")
    else:
        st.write("There is some relationship between age and marks.")

    st.markdown("### 🔵 Scatter: Attendance vs Marks (coloured by Department)")

    fig9, ax9 = plt.subplots(figsize=(8, 5))

    departments = df["Department"].unique()
    colors_list = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3"]

    for i, dept in enumerate(departments):
        dept_data = df[df["Department"] == dept]
        ax9.scatter(
            dept_data["Attendance"],
            dept_data["Marks"],
            label=dept,
            alpha=0.7,
            color=colors_list[i % len(colors_list)],
            s=60,
            edgecolors="white",
            linewidths=0.3
        )

    ax9.set_title("Attendance vs Marks (by Department)", fontsize=13, fontweight="bold")
    ax9.set_xlabel("Attendance (%)")
    ax9.set_ylabel("Marks")
    ax9.legend(title="Department")
    ax9.grid(True, linestyle="--", alpha=0.4)

    st.pyplot(fig9)
    plt.close(fig9)


st.markdown("---")
st.markdown(
    "🎓 **Student Analytics Dashboard** | "
    "Built with Python · Pandas · NumPy · Matplotlib · Seaborn · Streamlit"
)
