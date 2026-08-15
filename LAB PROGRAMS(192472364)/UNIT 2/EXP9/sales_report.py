import sqlite3
import pandas as pd


DATABASE = "sales.db"
OUTPUT_FILE = "sales_report.xlsx"


def get_category_revenue(database: str) -> pd.DataFrame:
    """Calculate category-wise revenue from valid orders."""

    query = """
    SELECT
        p.category AS category,
        SUM(
            oi.qty * p.unit_price *
            (1 - oi.discount_pct / 100.0)
        ) AS revenue
    FROM order_items oi
    JOIN products p
        ON oi.prod_id = p.prod_id
    JOIN orders o
        ON oi.order_id = o.order_id
    WHERE o.status <> 'CANCELLED'
    GROUP BY p.category
    ORDER BY revenue DESC;
    """

    with sqlite3.connect(database) as connection:
        dataframe = pd.read_sql_query(query, connection)

    return dataframe


def export_to_excel(
    dataframe: pd.DataFrame,
    output_file: str
) -> None:
    """Export the revenue summary to Excel with a bar chart."""

    with pd.ExcelWriter(
        output_file,
        engine="openpyxl"
    ) as writer:

        dataframe.to_excel(
            writer,
            sheet_name="Revenue Summary",
            index=False
        )

        worksheet = writer.sheets["Revenue Summary"]

        chart = dataframe.plot.bar(
            x="category",
            y="revenue",
            legend=False,
            title="Category-wise Revenue"
        ).get_figure()

        chart.savefig("category_revenue_chart.png")
        chart.clear()


def main() -> None:
    """Generate the category-wise sales report."""

    dataframe = get_category_revenue(DATABASE)

    print("\nCategory-wise Revenue")
    print("=" * 40)
    print(dataframe.to_string(index=False))

    export_to_excel(
        dataframe,
        OUTPUT_FILE
    )

    print("\nExcel report created successfully.")
    print("File:", OUTPUT_FILE)


if __name__ == "__main__":
    main()