import os

TRANSACTION_FILE = "transactions.csv"

#Dependency check helper
def check_dependencies() -> bool:
    missing_dependencies = []
    try:
        import pandas
    except ImportError:
        missing_dependencies.append("pandas")
    try:
        import plotly
    except ImportError:
        missing_dependencies.append("plotly")
    try:
        import numpy
    except ImportError:
        missing_dependencies.append("numpy")

    if missing_dependencies:
        print("\n Missing required libraries:", ", ".join(missing_dependencies))
        print("  Install them in PyCharm:")
        print("  File > Settings > Project > Python Interpreter > + (Add Package)")
        for lib in missing_dependencies:
            print(f" Search and install: {lib}")
        return False
    return True

#Trend Graph
def show_trend_graph() -> None:
    if not check_dependencies():
        return

    import pandas as pd
    import numpy as np
    import plotly.graph_objects as go

    #Load data
    if not os.path.exists(TRANSACTION_FILE):
        print("\n No transaction file found.")
        return

    df = pd.read_csv(TRANSACTION_FILE)

    #Keep only issue transactions (type == "1")
    issues_df = df[df["type"].astype(str) == "1"].copy()

    if issues_df.empty:
        print("\n No transaction data found. Issue some books first.")
        return

    #Parse and aggregate
    #parse dates with the DD/MM/YYYY format used throughout the system
    issues_df["date"] = pd.to_datetime(issues_df["date"], format="%d/%m/%Y")

    #Count issues per date
    daily_counts = (
        issues_df.groupby("date")
        .size()
        .reset_index(name="books_issued")
        .sort_values("date")
    )

    #Use numpy to compute a simple moving average trend line (window=2)
    counts = daily_counts["books_issued"].values.astype(float)
    window = min(2, len(counts)) #window can't exceed data length
    moving_average = np.convolve(counts, np.ones(window) / window, mode="same")

    #Format dates back to DD/MM/YYYY for display on x-axis
    date_labels = daily_counts["date"].dt.strftime("%d/%m/%Y").tolist()

    #Build plotly figure
    fig = go.Figure()

    #Bar chart - books issued per day
    fig.add_trace(go.Bar(
        x=date_labels,
        y=daily_counts["books_issued"].tolist(),
        name="books Issued",
        marker_color="#4f86c6",
        opacity=0.85,
    ))

    #Trend line - numpy moving average
    fig.add_trace(go.Scatter(
        x=date_labels,
        y=moving_average.tolist(),
        name="Trend (Moving Average)",
        mode="lines+markers",
        line=dict(color="#e05c2a", width=2, dash="dash"),
        marker=dict(size=6),
    ))


    #Layout
    fig.update_layout(
        title=dict(
            text="Books Issued Per Day - Library Trend",
            font=dict(size=20),
        ),
        xaxis=dict(
            title="Date",
            tickangle=-35,
        ),
        yaxis=dict(
            title="Number of Books Issued",
            dtick=1,
            rangemode="tozero",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        bargap=0.3,
        plot_bgcolor="white",
        paper_bgcolor="white",
        hovermode="x unified",
    )

    #summary stats printed to console
    total_issued = int(daily_counts["books_issued"].sum())
    busiest_date = date_labels[int(daily_counts["books_issued"].idxmax())]
    busiest_count = int(daily_counts["books_issued"].max())

    print(f"\n Trend Graph Summary")
    print(f"  Total books issued  : {total_issued}")
    print(f"  Days with activity  : {len(daily_counts)}")
    print(f"  Busiest day         : {busiest_date} ({busiest_count} books)")
    print(f"\n  Opening graph in your browser...")

    fig.show()

#Trend Graph Menu
def graph_menu() -> None:
    while True:
        print("\n=== Trend Graph ===")
        print("  1. Show Books Issued by Date")
        print("  0. Back to Main Menu")
        choice = input("Select option: ").strip()

        if choice == "1":
            show_trend_graph()
        elif choice == "0":
            break
        else:
            print("Invalid Selection. Try again.")

