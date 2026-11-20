"""10 validation tests for the cleaned retail dataset.
Run from the project folder:  pytest tests/ -v
"""
import pandas as pd, numpy as np, pytest

@pytest.fixture(scope="module")
def df():
    return pd.read_csv("cleaned_retail_customer_sales_dataset.csv",
                       parse_dates=["Order_Date", "Delivery_Date"])

def test_01_row_count_and_unique_ids(df):
    assert len(df) == 7000
    assert df.Transaction_ID.is_unique

def test_02_no_duplicate_rows(df):
    assert df.duplicated().sum() == 0

def test_03_gender_standardised(df):
    assert set(df.Gender.unique()) == {"Male", "Female"}

def test_04_region_standardised(df):
    assert set(df.Region.unique()) == {"North", "South", "East", "West"}

def test_05_age_valid_and_complete(df):
    assert df.Age.isna().sum() == 0
    assert df.Age.between(18, 100).all()
    assert df.Income.isna().sum() == 0 and (df.Income > 0).all()

def test_06_discount_valid_and_complete(df):
    assert df.Discount.isna().sum() == 0
    assert df.Discount.between(0, 0.5).all()

def test_07_dates_are_datetime_in_range(df):
    assert pd.api.types.is_datetime64_any_dtype(df.Order_Date)
    assert pd.api.types.is_datetime64_any_dtype(df.Delivery_Date)
    assert df.Order_Date.notna().all()
    assert df.Order_Date.min() >= pd.Timestamp("2023-01-01")
    assert df.Order_Date.max() <= pd.Timestamp("2024-12-31")

def test_08_delivery_never_before_order(df):
    assert (df.Delivery_Days.dropna() >= 0).all()
    assert (df.Delivery_Date.dropna() >= df.loc[df.Delivery_Date.notna(), "Order_Date"]).all()

def test_09_sales_formula_holds(df):
    calc = df.Quantity * df.Unit_Price * (1 - df.Discount)
    assert ((calc - df.Sales).abs() / df.Sales).max() < 0.02   # 2% tolerance (discount stored to 2 decimals)

def test_10_profit_reconciles_and_margin_valid(df):
    assert (df.Sales - df.Cost - df.Profit).abs().max() < 0.01
    assert df["Profit_Margin_%"].between(0, 100).all()

def test_11_age_group_labels_match_boundaries(df):
    assert df.loc[df.Age.between(46, 55), "Age_Group"].eq("46-55").all()
    assert df.loc[df.Age >= 56, "Age_Group"].eq("56+").all()
