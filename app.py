import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import plotly.graph_objects as go # pip install plotly graph_objects

st.set_page_config(page_title="Customer Shopping Exploratory Data Analysis (EDA)", page_icon=":bar_chart:", layout="wide")

# ---- READ CSV ----
@st.cache_data 
def get_data_from_csv():
    data = pd.read_csv('customer_shopping_data.csv')
    
    data['invoice_date'] = data['invoice_date'].astype('datetime64') 
    data['year'] = data['invoice_date'].dt.strftime("%Y")
    data['month'] = data['invoice_date'].dt.strftime("%m")
    data['weekday'] = data['invoice_date'].dt.strftime("%w")
    data['day'] = data['invoice_date'].dt.strftime("%d")
    #We will add a new column called age_category to the dataset.
    data['age_category'] = data['age'].apply(age_cat)
    #We will add a new column called total_price to the dataset.
    data['total_price'] = data['quantity'] * data['price']
    return data

def age_cat(age):
    if age <=30:
        age= 'young'
    elif age >30 and age <=50:
        age= 'middle'
    else:
        age= 'old'
    return age
data = get_data_from_csv()

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
shopping_mall = st.sidebar.multiselect(
    "Select the Shopping Mall:",
    options=data["shopping_mall"].unique(),
    default=data["shopping_mall"].unique()
)

age_category = st.sidebar.multiselect(
    "Select the Age Category:",
    options=data["age_category"].unique(),
    default=data["age_category"].unique(),
)

gender = st.sidebar.multiselect(
    "Select the gender:",
    options=data["gender"].unique(),
    default=data["gender"].unique()
)

data_selection = data.query(
    "shopping_mall == @shopping_mall & age_category ==@age_category & gender == @gender"
)

# ---- MAINPAGE ----
st.title(":bar_chart: Shopping Malls Exploratory Data Analysis in Istanbul")
st.markdown("##")

# TOP KPI's
total_sales = int(data_selection["total_price"].sum())


average_sale_by_transaction = round(data_selection["total_price"].mean(), 2)

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"TL ₺ {total_sales:,}")
    
    
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"TL ₺ {average_sale_by_transaction}")

st.markdown("""---""")

# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = (
    data_selection.groupby(by=["category"]).sum()[["total_price"]].sort_values(by="total_price")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x="total_price",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# SALES BY DAY [BAR CHART]
sales_by_day = data_selection.groupby(by=["day"]).sum()[["total_price"]]
fig_daily_sales = px.bar(
    sales_by_day,
    x=sales_by_day.index,
    y="total_price",
    title="<b>Sales by day</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_day),
    template="plotly_white",
)

sales_by_month = data_selection.groupby(by=["month"]).sum()[["total_price"]]
fig_monthly_sales = px.bar(
    sales_by_month,
    x=sales_by_month.index,
    y="total_price",
    title="<b>Sales by month</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_month),
    template="plotly_white",
)

fig_daily_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

gender_count = data_selection['gender'].value_counts()
fig_pie = px.pie(
    gender_count, 
    values = gender_count, 
    hole = 0.4,
    names = gender_count.index, 
   # color = gender_count.index,
    title = 'Gender',
    color_discrete_map = {'female':'#71b0df', 'male': '#d90718'},
    template="plotly_white",
)
pay_method	= data_selection['payment_method'].value_counts()
fig_donut = px.pie(
    pay_method	, 
    values = pay_method, 
    hole = 0.4,
    names = pay_method.index, 
    #color = pay_method,
    title = 'Payment Method	',
    color_discrete_map = {'Debit Card':'#cyan', 'Credit Card': '#green', 'Cash': '#red'},
    template="plotly_white",
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_daily_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)


left_column1, right_column1 = st.columns(2)
left_column1.plotly_chart(fig_pie, use_container_width=True)
right_column1.plotly_chart(fig_monthly_sales, use_container_width=True)

left_column2, right_column2 = st.columns(2)
#left_column1.plotly_chart(fig_pie, use_container_width=True)
right_column1.plotly_chart(fig_donut, use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)