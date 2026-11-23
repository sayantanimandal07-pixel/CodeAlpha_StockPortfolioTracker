import csv
from decimal import Decimal

STOCK_PRICES = {
    "AAPL": Decimal("180.00"),
    "TSLA": Decimal("250.00"),
    "GOOGL": Decimal("140.00"),
    "MSFT": Decimal("330.00"),
    "AMZN": Decimal("135.00"),
}

def create_table(headers, rows, right_align=()):
    """Build an aligned table with borders."""
    headers = [str(header) for header in headers]
    rows = [[str(cell) for cell in row] for row in rows]

    widths = [
        max(len(headers[i]), max(
            (len(row[i]) for row in rows), default=0
        ))
        for i in range(len(headers))
    ]

    border = "+" + "+".join(
        "-" * (width + 2) for width in widths
    ) + "+"

    def format_row(row):
        cells = []

        for i, cell in enumerate(row):
            if i in right_align:
                cells.append(f" {cell:>{widths[i]}} ")
            else:
                cells.append(f" {cell:<{widths[i]}} ")

        return "|" + "|".join(cells) + "|"

    lines = [border, format_row(headers), border]

    for row in rows:
        lines.append(format_row(row))

    lines.append(border)
    return "\n".join(lines)

def display_stocks():
    rows = [
        [index, symbol, f"{price:,.2f}"]
        for index, (symbol, price) in enumerate(
            STOCK_PRICES.items(), start=1
        )
    ]

    print("\nAVAILABLE STOCKS\n")
    print(create_table(
        ["No.", "Symbol", "Price (USD)"],
        rows,
        right_align=(0, 2),
    ))


def build_portfolio_report(portfolio):
    rows = []
    total = Decimal("0.00")

    for index, (symbol, quantity) in enumerate(
        portfolio.items(), start=1
    ):
        price = STOCK_PRICES[symbol]
        value = price * quantity
        total += value

        rows.append([
            index,
            symbol,
            quantity,
            f"{price:,.2f}",
            f"{value:,.2f}",
        ])

    # A blank row separates the holdings from the total.
    rows.append(["", "", "", "", ""])
    rows.append([
        "",
        "TOTAL",
        sum(portfolio.values()),
        "",
        f"{total:,.2f}",
    ])

    table = create_table(
        ["No.", "Stock", "Quantity", "Price (USD)", "Value (USD)"],
        rows,
        right_align=(0, 2, 3, 4),
    )

    report = "STOCK PORTFOLIO REPORT\n\n" + table
    return report, total


def save_portfolio(portfolio, report, total, file_format):
    filename = f"portfolio.{file_format}"

    try:
        if file_format == "txt":
            with open(filename, "w", encoding="utf-8") as file:
                file.write(report + "\n")

        else:
            with open(filename, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)

                writer.writerow([
                    "No.",
                    "Stock",
                    "Quantity",
                    "Price (USD)",
                    "Value (USD)",
                ])

                for index, (symbol, quantity) in enumerate(
                    portfolio.items(), start=1
                ):
                    price = STOCK_PRICES[symbol]

                    writer.writerow([
                        index,
                        symbol,
                        quantity,
                        f"{price:.2f}",
                        f"{price * quantity:.2f}",
                    ])

                writer.writerow([
                    "",
                    "TOTAL",
                    sum(portfolio.values()),
                    "",
                    f"{total:.2f}",
                ])

        print(f"\nReport saved successfully: {filename}")

    except OSError as error:
        print(f"\nCould not save the report: {error}")

def main():
    portfolio = {}

    print("=" * 60)
    print("STOCK PORTFOLIO TRACKER".center(60))
    print("=" * 60)

    display_stocks()

    while True:
        symbol = input(
            "\nEnter stock symbol (or 'done' to finish): "
        ).strip().upper()

        if symbol == "DONE":
            break

        if symbol not in STOCK_PRICES:
            print("Invalid symbol. Please select a stock from the table.")
            continue

        while True:
            try:
                quantity = int(input(f"Enter quantity for {symbol}: "))

                if quantity <= 0:
                    print("Please enter a quantity greater than zero.")
                    continue

                break

            except ValueError:
                print("Invalid input. Please enter a whole number.")

        portfolio[symbol] = portfolio.get(symbol, 0) + quantity
        print(f"Added: {quantity} share(s) of {symbol}")

    if not portfolio:
        print("\nNo stocks were added.")
        return

    report, total = build_portfolio_report(portfolio)
    print("\n" + report)

    while True:
        file_format = input(
            "\nSave report as 'txt' / 'csv', or enter 'no': "
        ).strip().lower()

        if file_format == "no":
            print("\nThank you for using the tracker!")
            break

        if file_format in ("txt", "csv"):
            save_portfolio(
                portfolio, report, total, file_format
            )
            break

        print("Please enter 'txt', 'csv', or 'no'.")


if __name__ == "__main__":
    main()