import os

def test_notebook_exists():
    notebook_path = "notebooks/01_eda_frutas.ipynb"
    assert os.path.isfile(notebook_path), f"Notebook not found at {notebook_path}"

def test_notebook_contains_markdown():
    notebook_path = "notebooks/01_eda_frutas.ipynb"
    with open(notebook_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Check for some expected markdown content
    assert "# Exploratory Data Analysis of Fruits Prices" in content, "Expected markdown title not found"
    assert "## Price Trends" in content, "Expected section 'Price Trends' not found"