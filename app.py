"""Retail Sales EDA - Streamlit Dashboard
Run:  streamlit run app.py
"""
import pandas as pd, numpy as np
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Retail Sales EDA", page_icon="📊", layout="wide")

@st.cache_data
def load():
    return pd.read_csv("cleaned_retail_customer_sales_dataset.csv", parse_dates=["Order_Date", "Delivery_Date"])

@st.cache_data
def load_raw():
    return pd.read_csv("retail_customer_sales_dataset.csv")

df = load()
st.title("📊 Retail Sales EDA Dashboard")
st.caption("7,000 cleaned transactions | India | 2023-2024 | use the sidebar filters")

# ---------------- Sidebar filters ----------------
st.sidebar.header("Filters")
years = st.sidebar.multiselect("Year", sorted(df.Order_Year.unique()), default=sorted(df.Order_Year.unique()))
regions = st.sidebar.multiselect("Region", sorted(df.Region.unique()), default=sorted(df.Region.unique()))
cats = st.sidebar.multiselect("Product category", sorted(df.Product_Category.unique()), default=sorted(df.Product_Category.unique()))
segs = st.sidebar.multiselect("Customer segment", sorted(df.Customer_Segment.unique()), default=sorted(df.Customer_Segment.unique()))
f = df[df.Order_Year.isin(years) & df.Region.isin(regions) & df.Product_Category.isin(cats) & df.Customer_Segment.isin(segs)]
if f.empty:
    st.warning("No data for this filter combination. Please widen the filters.")
    st.stop()

# ---------------- KPIs ----------------
c = st.columns(6)
c[0].metric("Total sales", f"₹{f.Sales.sum()/1e5:,.1f} L")
c[1].metric("Total profit", f"₹{f.Profit.sum()/1e5:,.1f} L")
c[2].metric("Profit margin", f"{f.Profit.sum()/f.Sales.sum()*100:.1f}%")
c[3].metric("Orders", f"{len(f):,}")
c[4].metric("Avg order value", f"₹{f.Sales.mean():,.0f}")
c[5].metric("Return rate", f"{(f.Returned=='Yes').mean()*100:.1f}%")

t1, t2, t3, t4, t5 = st.tabs(["📈 Overview", "📊 Distributions & Outliers", "💡 Business Insights", "🧹 Data Quality", "🔎 Data Explorer"])

# ---------------- Overview ----------------
with t1:
    m = f.groupby("Order_Month").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).reset_index()
    st.plotly_chart(px.line(m, x="Order_Month", y=["Sales", "Profit"], markers=True, title="Monthly sales and profit"), width='stretch')
    a, b = st.columns(2)
    cs = f.groupby("Product_Category").Sales.sum().sort_values().reset_index()
    a.plotly_chart(px.bar(cs, x="Sales", y="Product_Category", orientation="h", title="Sales by category"), width='stretch')
    rg = f.groupby("Region").Sales.sum().reset_index()
    b.plotly_chart(px.pie(rg, names="Region", values="Sales", hole=.45, title="Sales share by region"), width='stretch')

# ---------------- Distributions & outliers ----------------
with t2:
    st.subheader("Distribution of a numeric variable")
    var = st.selectbox("Choose variable", ["Sales", "Profit", "Income", "Age", "Unit_Price", "Quantity", "Discount", "Profit_Margin_%"])
    a, b = st.columns(2)
    fig = px.histogram(f, x=var, nbins=50, title=f"{var}: histogram")
    fig.add_vline(x=f[var].mean(), line_dash="dash", line_color="red", annotation_text="mean")
    fig.add_vline(x=f[var].median(), line_color="green", annotation_text="median")
    a.plotly_chart(fig, width='stretch')
    b.plotly_chart(px.box(f, y=var, title=f"{var}: box plot"), width='stretch')
    q1, q3 = f[var].quantile([.25, .75]); iqr = q3 - q1
    out = ((f[var] < q1 - 1.5*iqr) | (f[var] > q3 + 1.5*iqr)).sum()
    s = st.columns(5)
    s[0].metric("Mean", f"{f[var].mean():,.2f}"); s[1].metric("Median", f"{f[var].median():,.2f}")
    s[2].metric("Std dev", f"{f[var].std():,.2f}"); s[3].metric("Skewness", f"{f[var].skew():.2f}")
    s[4].metric("IQR outliers", f"{out:,}")
    st.info("Skewness above 0.5 means right-skewed: a few very large values pull the mean above the median, so the median is the fairer 'typical' value.")

# ---------------- Business insights ----------------
with t3:
    a, b = st.columns(2)
    d = f.assign(Margin=f.Profit).groupby("Product_Category").agg(S=("Sales", "sum"), P=("Profit", "sum")).reset_index()
    d["Margin %"] = d.P/d.S*100
    a.plotly_chart(px.bar(d, x="Product_Category", y="Margin %", title="Profit margin % by category (nearly identical)"), width='stretch')
    dm = f.groupby("Delivery_Mode").Delivery_Days.mean().reset_index()
    b.plotly_chart(px.bar(dm, x="Delivery_Mode", y="Delivery_Days", title="Average recorded delivery days by mode"), width='stretch')
    a, b = st.columns(2)
    db = f.groupby("Discount_Band", observed=True).agg(Margin=("Profit_Margin_%", "mean"), Qty=("Quantity", "mean")).reset_index()
    a.plotly_chart(px.bar(db, x="Discount_Band", y="Qty", title="Average quantity by discount band"), width='stretch')
    rr = f.assign(R=(f.Returned == "Yes")*100).groupby("Product_Category").R.mean().reset_index()
    b.plotly_chart(px.bar(rr, x="Product_Category", y="R", title="Return rate % by category"), width='stretch')
    st.markdown("""**Key takeaways (full data):** Electronics + Furniture give 83% of sales. Discount has near-zero correlation with quantity (-0.001) and margin (-0.005) in this dataset; this does not establish a causal effect.
Recorded average delivery times are similar across modes (~5.6-5.8 days); verify date quality and service definitions before concluding the modes are equivalent. 12.6% of orders are returned. Sales fell 1.5% in 2024.""")
    top = f.groupby("Customer_ID").Sales.sum().nlargest(10).reset_index()
    st.subheader("Top 10 customers"); st.dataframe(top, width='stretch', hide_index=True)

# ---------------- Data quality ----------------
with t4:
    raw = load_raw()
    st.subheader("Before vs after cleaning")
    q = st.columns(4)
    q[0].metric("Rows", f"{len(df):,}", f"{len(df)-len(raw):,} duplicates removed")
    q[1].metric("Gender spellings", "2", "from 8"); q[2].metric("Region spellings", "4", "from 12"); q[3].metric("Date formats", "1", "from 4")
    miss = pd.DataFrame({"Missing (raw)": raw.isna().sum(), "Missing % (raw)": (raw.isna().mean()*100).round(2)})
    miss = miss[miss["Missing (raw)"] > 0]
    st.plotly_chart(px.bar(miss.reset_index(), x="index", y="Missing (raw)", title="Missing values in the raw file"), width='stretch')
    st.markdown("""| Issue | Fix |
|---|---|
| Duplicate transactions | Removed, kept most complete copy |
| Impossible Age / Discount | Age from the same customer's other orders; Discount recomputed from the Sales formula |
| Missing Income | Customer's own value, else segment median |
| Delivery before order | Date blanked, order kept |
| Missing rating / satisfaction | Kept as 'not rated' / 'Not Recorded' |""")

# ---------------- Explorer ----------------
with t5:
    st.write(f"Showing {len(f):,} rows")
    st.dataframe(f.head(500), width='stretch')
    st.download_button("⬇ Download filtered data (CSV)", f.to_csv(index=False).encode(), "filtered_sales.csv", "text/csv")
