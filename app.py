import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Exploratory Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Exploratory Analysis with a Finding")
st.subheader("Does offering higher discounts affect profitability?")

st.write(
    "Upload the Sample Superstore CSV dataset to explore "
    "the relationship between discounts and profit."
)

uploaded_file = st.file_uploader(
    "Upload Sample - Superstore.csv",
    type=["csv"]
)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding="latin1")
        df.columns = df.columns.str.strip()

        required = ["Sales", "Profit", "Discount"]
        missing = [col for col in required if col not in df.columns]

        if missing:
            st.error("Missing required columns: " + ", ".join(missing))
        else:
            for col in required:
                df[col] = pd.to_numeric(df[col], errors="coerce")

            df = df.dropna(subset=required)

            c1, c2, c3 = st.columns(3)
            c1.metric("Total Sales", f"${df['Sales'].sum():,.2f}")
            c2.metric("Total Profit", f"${df['Profit'].sum():,.2f}")
            c3.metric("Average Discount", f"{df['Discount'].mean():.1%}")

            st.subheader("Discount vs Profit")

            fig, ax = plt.subplots()
            ax.scatter(df["Discount"], df["Profit"], alpha=0.4)
            ax.set_xlabel("Discount")
            ax.set_ylabel("Profit")
            ax.set_title("Does higher discount affect profit?")
            ax.axhline(0, linewidth=1)
            st.pyplot(fig)
            plt.close(fig)

            st.subheader("Profit by Discount Level")

            bins = [-0.001, 0, 0.10, 0.20, 0.30, 0.50, 1.0]
            labels = [
                "No discount", "0–10%", "10–20%",
                "20–30%", "30–50%", "50–100%"
            ]

            df["Discount_Level"] = pd.cut(
                df["Discount"],
                bins=bins,
                labels=labels,
                include_lowest=True
            )

            summary = df.groupby(
                "Discount_Level", observed=False
            ).agg(
                Orders=("Profit", "size"),
                Total_Sales=("Sales", "sum"),
                Total_Profit=("Profit", "sum"),
                Average_Profit=("Profit", "mean")
            ).reset_index()

            st.dataframe(summary, use_container_width=True)

            fig2, ax2 = plt.subplots()
            ax2.bar(
                summary["Discount_Level"].astype(str),
                summary["Total_Profit"]
            )
            ax2.set_xlabel("Discount Level")
            ax2.set_ylabel("Total Profit")
            ax2.set_title("Total Profit by Discount Level")
            plt.xticks(rotation=30, ha="right")
            st.pyplot(fig2)
            plt.close(fig2)

            st.subheader("Category Analysis")

            if "Category" in df.columns:
                category = df.groupby("Category").agg(
                    Total_Sales=("Sales", "sum"),
                    Total_Profit=("Profit", "sum")
                ).reset_index()

                st.dataframe(category, use_container_width=True)

            st.subheader("Key Finding")
            st.write(
                "Compare total and average profit across discount levels. "
                "Higher discounts may be associated with lower profit, "
                "but the dataset results should be checked before drawing "
                "a final conclusion."
            )

            st.download_button(
                "Download Discount Analysis CSV",
                summary.to_csv(index=False).encode("utf-8"),
                "discount_profit_analysis.csv",
                "text/csv"
            )

    except Exception as e:
        st.error(f"Could not read the dataset: {e}")
else:
    st.info("Upload your Sample Superstore CSV file to begin.")

