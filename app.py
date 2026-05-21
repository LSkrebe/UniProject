"""CLI entry point for the Document Analyzer."""

import sys

from application import DocumentAnalyzerApp


def print_menu():
    print("\nDocument Analyzer")
    print("1. Analyze URL or text file")
    print("2. View saved history")
    print("3. Export history to CSV")
    print("4. Exit")


def print_history(app):
    history = app.get_history()
    if not history:
        print("\nNo saved analyses yet.")
        return
    print(f"\nSaved analyses: {len(history)}")
    for index, item in enumerate(history, start=1):
        print(f"\n--- #{index} ---")
        print(app.format_result(item))


def main():
    app = DocumentAnalyzerApp()

    while True:
        print_menu()
        choice = input("Choice: ").strip()

        if choice == "1":
            source = input("URL or file path: ").strip()
            if not source:
                print("Input cannot be empty.")
                continue
            try:
                print("\nLoading document...")
                result = app.analyze_input(source)
                print(app.format_result(result))
                print("Saved to data/analysis_history.json")
            except (ValueError, FileNotFoundError) as error:
                print(f"Error: {error}")
            except Exception as error:
                print(f"Error: {error}")

        elif choice == "2":
            print_history(app)

        elif choice == "3":
            try:
                path = app.export_history_csv()
                print(f"Exported to {path}")
            except Exception as error:
                print(f"Error: {error}")

        elif choice == "4":
            print("Goodbye.")
            sys.exit(0)

        else:
            print("Invalid choice. Enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
