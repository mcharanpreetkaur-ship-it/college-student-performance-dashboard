import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# COLLEGE STUDENT PERFORMANCE DASHBOARD
# -------------------------------
# 1. LOAD EXCEL FILE

file_path = "students data.xlsx"

try:
    df = pd.read_excel(file_path)
    print("Excel file loaded successfully!")
except Exception as e:
    print("Error loading Excel file:", e)
    input("Press Enter to exit...")
    exit()


# Remove unnecessary index column if present
if "index" in df.columns:
    df = df.drop(columns=["index"])

# Remove accidental spaces from column names
df.columns = df.columns.str.strip()

print("\nColumns found in Excel:")
print(list(df.columns))

required_columns = [
    "Student",
    "Semester",
    "Attendance",
    "Business Maths",
    "Financial Management",
    "Marketing",
    "HRM",
    "Study Hours",
    "Assignment Completion",
    "Average Marks",
    "GPA",
    "Grade"
]

missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    print("\nMissing columns:")
    print(missing_columns)
    input("\nPress Enter to exit...")
    exit()

numeric_columns = [
    "Semester",
    "Attendance",
    "Business Maths",
    "Financial Management",
    "Marketing",
    "HRM",
    "Study Hours",
    "Assignment Completion",
    "Average Marks",
    "GPA"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")


# ============================================================
# DASHBOARD FUNCTION
# ============================================================

def create_dashboard(data):

    # --------------------------------------------------------
    # BASIC VALUES
    # --------------------------------------------------------

    total_students = len(data)

    avg_attendance = data["Attendance"].mean()
    avg_marks = data["Average Marks"].mean()
    avg_gpa = data["GPA"].mean()

 
    fig = plt.figure(figsize=(18, 10))

    # Dusty peach background
    fig.patch.set_facecolor("#E8C9B8")

    # --------------------------------------------------------
    # MAIN GRID
    # --------------------------------------------------------

    gs = fig.add_gridspec(
        3,
        4,
        width_ratios=[0.75, 1.25, 1.25, 1.25],
        height_ratios=[0.65, 1.45, 1.45],
        hspace=0.55,
        wspace=0.35
    )

    # ========================================================
    # TITLE
    # ========================================================

    fig.text(
        0.58,
        0.965,
        "COLLEGE STUDENT PERFORMANCE DASHBOARD",
        ha="center",
        va="center",
        fontsize=22,
        fontweight="bold",
        family="DejaVu Sans"
    )

    fig.text(
        0.58,
        0.935,
        "Academic Performance • Attendance • Learning Behaviour",
        ha="center",
        va="center",
        fontsize=11,
        family="DejaVu Sans"
    )


    # ========================================================
    # STUDENT BOX - LEFT SIDE
    # ========================================================

    student_ax = fig.add_subplot(gs[1:, 0])

    student_ax.set_facecolor("#F7EEE9")

    student_ax.set_xticks([])
    student_ax.set_yticks([])

    for spine in student_ax.spines.values():
        spine.set_linewidth(1.5)

    student_ax.set_title(
        "STUDENTS",
        fontsize=13,
        fontweight="bold",
        pad=10
    )

    students = list(data["Student"])

    # Compact student list
    y_position = 0.92

    for i, student in enumerate(students, start=1):

        student_ax.text(
            0.08,
            y_position,
            f"{i}. {student}",
            fontsize=9.5,
            family="DejaVu Sans",
            va="top"
        )

        y_position -= 0.075

    student_ax.text(
        0.08,
        0.04,
        f"Total: {total_students} students",
        fontsize=9,
        fontweight="bold"
    )


    # ========================================================
    # KPI CARDS
    # ========================================================

    kpi_positions = [
        (0.25, 0.83),
        (0.43, 0.83),
        (0.61, 0.83),
        (0.79, 0.83)
    ]

    kpi_titles = [
        "TOTAL STUDENTS",
        "AVG ATTENDANCE",
        "AVG MARKS",
        "AVG GPA"
    ]

    kpi_values = [
        f"{total_students}",
        f"{avg_attendance:.1f}%",
        f"{avg_marks:.1f}",
        f"{avg_gpa:.2f}"
    ]

    for (x, y), title, value in zip(
        kpi_positions,
        kpi_titles,
        kpi_values
    ):

        fig.text(
            x,
            y,
            f"{title}\n\n{value}",
            ha="center",
            va="center",
            fontsize=11,
            fontweight="bold",
            bbox=dict(
                boxstyle="round,pad=0.7",
                facecolor="#F7EEE9",
                edgecolor="#B9795B",
                linewidth=1.5
            )
        )


    # ========================================================
    # GRAPH 1
    # SUBJECT-WISE AVERAGE MARKS
    # ========================================================

    ax1 = fig.add_subplot(gs[1, 1:3])

    subjects = [
        "Business Maths",
        "Financial Management",
        "Marketing",
        "HRM"
    ]

    subject_averages = [
        data["Business Maths"].mean(),
        data["Financial Management"].mean(),
        data["Marketing"].mean(),
        data["HRM"].mean()
    ]

    bars = ax1.bar(
        subjects,
        subject_averages,
        width=0.55,
        color="#B96F4A"
    )

    ax1.set_title(
        "Subject-wise Average Marks",
        fontsize=13,
        fontweight="bold",
        pad=12
    )

    ax1.set_ylabel("Average Marks")
    ax1.set_ylim(0, 100)

    ax1.tick_params(axis="x", rotation=0)

    for bar, value in zip(bars, subject_averages):
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            value + 1,
            f"{value:.1f}",
            ha="center",
            fontsize=9,
            fontweight="bold"
        )

    ax1.grid(axis="y", alpha=0.2)


    # ========================================================
    # GRAPH 2
    # ATTENDANCE VS GPA
    # ========================================================

    ax2 = fig.add_subplot(gs[1, 3])

    ax2.scatter(
        data["Attendance"],
        data["GPA"],
        s=70,
        color="#9A5B3D"
    )

    ax2.set_title(
        "Attendance vs GPA",
        fontsize=13,
        fontweight="bold",
        pad=12
    )

    ax2.set_xlabel("Attendance (%)")
    ax2.set_ylabel("GPA")

    ax2.grid(alpha=0.2)

    # Student labels
    for _, row in data.iterrows():

        ax2.annotate(
            row["Student"],
            (
                row["Attendance"],
                row["GPA"]
            ),
            xytext=(4, 4),
            textcoords="offset points",
            fontsize=7
        )


    # ========================================================
    # GRAPH 3
    # STUDY HOURS VS AVERAGE MARKS
    # ========================================================

    ax3 = fig.add_subplot(gs[2, 1:3])

    ax3.scatter(
        data["Study Hours"],
        data["Average Marks"],
        s=75,
        color="#B96F4A"
    )

    ax3.set_title(
        "Study Hours vs Average Marks",
        fontsize=13,
        fontweight="bold",
        pad=12
    )

    ax3.set_xlabel("Study Hours")
    ax3.set_ylabel("Average Marks")

    ax3.grid(alpha=0.2)

    for _, row in data.iterrows():

        ax3.annotate(
            row["Student"],
            (
                row["Study Hours"],
                row["Average Marks"]
            ),
            xytext=(4, 4),
            textcoords="offset points",
            fontsize=7
        )


    # ========================================================
    # GRAPH 4
    # GRADE DISTRIBUTION
    # ========================================================

    ax4 = fig.add_subplot(gs[2, 3])

    grade_order = ["A+", "A", "B", "C", "D", "F"]

    grade_counts = (
        data["Grade"]
        .value_counts()
        .reindex(grade_order, fill_value=0)
    )

    bars = ax4.bar(
        grade_counts.index,
        grade_counts.values,
        width=0.55,
        color="#9A5B3D"
    )

    ax4.set_title(
        "Grade Distribution",
        fontsize=13,
        fontweight="bold",
        pad=12
    )

    ax4.set_xlabel("Grade")
    ax4.set_ylabel("Number of Students")

    ax4.set_ylim(
        0,
        max(grade_counts.values) + 1
    )

    for bar, value in zip(
        bars,
        grade_counts.values
    ):

        ax4.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.05,
            str(value),
            ha="center",
            fontsize=10,
            fontweight="bold"
        )

    ax4.grid(axis="y", alpha=0.2)


    # ========================================================
    # FOOTER
    # ========================================================

    fig.text(
        0.58,
        0.025,
        "Data Analysis using Python • Pandas • Matplotlib",
        ha="center",
        fontsize=9
    )


    # ========================================================
    # FINAL SPACING
    # ========================================================

    plt.subplots_adjust(
        left=0.04,
        right=0.97,
        top=0.88,
        bottom=0.07
    )

    plt.show()


# ============================================================
# FILTER / INTERACTION
# ============================================================

while True:

    print("\n" + "=" * 55)
    print("       COLLEGE STUDENT PERFORMANCE DASHBOARD")
    print("=" * 55)

    print("\nSemester Options:")
    print("0 - All Semesters")
    print("1 - Semester 1")
    print("2 - Semester 2")
    print("3 - Semester 3")
    print("4 - Semester 4")
    print("5 - Semester 5")
    print("6 - Semester 6")

    try:
        semester_choice = int(
            input("\nSelect Semester (0-6): ")
        )
    except:
        print("Please enter a number from 0 to 6.")
        continue


    # --------------------------------------------------------
    # SEMESTER FILTER
    # --------------------------------------------------------

    filtered_df = df.copy()

    if semester_choice != 0:

        filtered_df = filtered_df[
            filtered_df["Semester"] == semester_choice
        ]


    # --------------------------------------------------------
    # ATTENDANCE FILTER
    # --------------------------------------------------------

    try:

        min_attendance = float(
            input("Enter minimum attendance (0 for no minimum): ")
        )

        max_attendance = float(
            input("Enter maximum attendance (100 for no maximum): ")
        )

    except:

        print("Please enter valid attendance numbers.")
        continue


    filtered_df = filtered_df[
        (filtered_df["Attendance"] >= min_attendance) &
        (filtered_df["Attendance"] <= max_attendance)
    ]


    # --------------------------------------------------------
    # STUDENT FILTER
    # --------------------------------------------------------

    student_choice = input(
        "\nEnter Student Name or type ALL: "
    ).strip()

    if student_choice.lower() != "all":

        filtered_df = filtered_df[
            filtered_df["Student"].str.lower()
            == student_choice.lower()
        ]


    # --------------------------------------------------------
    # CHECK DATA
    # --------------------------------------------------------

    if filtered_df.empty:

        print("\nNo students match your selected filters.")

    else:

        print(
            f"\nDashboard created for "
            f"{len(filtered_df)} student(s)."
        )

        create_dashboard(filtered_df)


    # --------------------------------------------------------
    # RUN AGAIN?
    # --------------------------------------------------------

    again = input(
        "\nDo you want to create another dashboard? (yes/no): "
    ).strip().lower()

    if again != "yes":
        print("\nDashboard closed. Thank you!")
        break
