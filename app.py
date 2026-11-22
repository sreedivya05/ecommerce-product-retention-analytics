import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="E-Commerce Product Analytics", page_icon="📊", layout="wide")
BASE = Path(__file__).parent

customers = pd.read_csv(BASE / "data/customers.csv", parse_dates=["signup_date"])
products = pd.read_csv(BASE / "data/products.csv")
orders = pd.read_csv(BASE / "data/orders.csv", parse_dates=["order_date"])
events = pd.read_csv(BASE / "data/events.csv", parse_dates=["event_date"])

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:Inter,sans-serif}
.stApp{background:#f5f7fb}
.block-container{max-width:1450px;padding:2rem 3rem 4rem}
section[data-testid="stSidebar"]{background:#0f172a}
section[data-testid="stSidebar"] *{color:#e5e7eb!important}
.hero{background:radial-gradient(circle at 90% 10%,rgba(99,102,241,.45),transparent 30%),linear-gradient(135deg,#0f172a,#172554 55%,#312e81);border-radius:24px;padding:34px 40px;color:white;box-shadow:0 18px 50px rgba(15,23,42,.18);margin-bottom:26px}
.hero-badge{display:inline-block;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);border-radius:999px;padding:7px 13px;font-size:12px;font-weight:800;margin-bottom:12px}
.hero h1{font-size:38px;margin:0 0 10px;font-weight:800}.hero p{color:#dbeafe;font-size:15px;max-width:850px}
.kpi{background:white;border:1px solid #e5e7eb;border-radius:17px;padding:19px 20px;min-height:120px;box-shadow:0 7px 22px rgba(15,23,42,.05)}
.kpi-label{color:#64748b;font-size:11px;font-weight:800;letter-spacing:.7px;text-transform:uppercase}
.kpi-value{color:#0f172a;font-size:27px;font-weight:800;margin-top:8px}.kpi-sub{color:#94a3b8;font-size:11px;margin-top:4px}
.card{background:white;border:1px solid #e5e7eb;border-radius:17px;padding:22px;box-shadow:0 7px 22px rgba(15,23,42,.04);margin-bottom:18px}
.insight{background:linear-gradient(90deg,#eef2ff,#f8fafc);border-left:4px solid #6366f1;padding:15px 18px;border-radius:10px;margin:10px 0;color:#334155}
.recommendation{background:white;border:1px solid #e2e8f0;border-radius:15px;padding:18px;margin-bottom:12px}
.recommendation .title{color:#111827;font-weight:800}.recommendation .body{color:#64748b;font-size:14px}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 📊 ProductLens")
    st.caption("E-Commerce Product Analytics")
    st.markdown("### 🎛️ Filters")
    min_date, max_date = orders.order_date.min().date(), orders.order_date.max().date()
    date_range = st.date_input("Order date", value=(min_date,max_date), min_value=min_date, max_value=max_date)
    categories = st.multiselect("Product category", sorted(products.category.unique()), default=sorted(products.category.unique()))
    cities = st.multiselect("Customer city", sorted(customers.city.unique()), default=[])
    st.markdown("---")
    st.caption("Change filters and the analysis updates across the dashboard.")

if isinstance(date_range, tuple) and len(date_range)==2:
    start_date,end_date=pd.Timestamp(date_range[0]),pd.Timestamp(date_range[1])
else:
    start_date,end_date=pd.Timestamp(min_date),pd.Timestamp(max_date)

allowed_products=products[products.category.isin(categories)].product_id
fo=orders[orders.order_date.between(start_date,end_date)&orders.product_id.isin(allowed_products)].copy()
if cities:
    allowed_customers=customers[customers.city.isin(cities)].customer_id
    fo=fo[fo.customer_id.isin(allowed_customers)]
fe=events[events.event_date.between(start_date,end_date)&events.product_id.isin(allowed_products)].copy()

st.markdown("""
<div class="hero">
<div class="hero-badge">PRODUCT ANALYTICS PORTFOLIO PROJECT</div>
<h1>E-Commerce Product & Customer Analytics</h1>
<p>Turn transaction and product-event data into product decisions: revenue performance, funnel conversion, repeat purchasing and product opportunities.</p>
</div>
""",unsafe_allow_html=True)

d=fo[fo.status=="Delivered"].copy()
revenue=d.revenue.sum(); order_count=d.order_id.nunique(); customer_count=d.customer_id.nunique()
aov=revenue/order_count if order_count else 0
views=(fe.event_type=="Viewed Product").sum(); purchases=(fe.event_type=="Purchased").sum()
event_conversion=100*purchases/views if views else 0
customer_orders=d.groupby("customer_id").order_id.nunique()
repeat_rate=100*customer_orders.ge(2).mean() if len(customer_orders) else 0

cols=st.columns(5)
for col,label,value,sub in zip(cols,
    ["Revenue","Orders","Customers","AOV","Repeat Rate"],
    [f"₹{revenue/100000:.2f}L",f"{order_count:,}",f"{customer_count:,}",f"₹{aov:,.0f}",f"{repeat_rate:.1f}%"],
    ["Delivered orders","Delivered","With delivered orders","Average order value","2+ delivered orders"]):
    col.markdown(f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-sub">{sub}</div></div>',unsafe_allow_html=True)

tab1,tab2,tab3,tab4,tab5=st.tabs(["📊 Overview","🔄 Funnel","👥 Retention","🛍️ Product Analysis","🗂️ Data Explorer"])

with tab1:
    st.subheader("Business Overview")
    st.caption("Start with business performance, then investigate product behavior.")
    a,b=st.columns(2)
    with a:
        st.markdown('<div class="card"><b>📈 Monthly Revenue</b>',unsafe_allow_html=True)
        st.line_chart(d.set_index("order_date").resample("ME").revenue.sum(),height=300)
        st.markdown("</div>",unsafe_allow_html=True)
    with b:
        st.markdown('<div class="card"><b>🏷️ Revenue by Category</b>',unsafe_allow_html=True)
        cat=d.merge(products,on="product_id").groupby("category").revenue.sum().sort_values(ascending=False)
        st.bar_chart(cat,height=300)
        st.markdown("</div>",unsafe_allow_html=True)
    top=cat.index[0] if len(cat) else "N/A"
    st.markdown(f'<div class="insight"><b>Business signal:</b> {top} is the largest revenue category in the selected period. Next investigate whether its traffic, conversion and repeat purchase behavior support that result.</div>',unsafe_allow_html=True)

with tab2:
    st.subheader("Product Funnel")
    st.caption("Find where users lose momentum between discovery and purchase.")
    order=["Viewed Product","Added to Cart","Checkout","Purchased"]
    funnel=fe.groupby("event_type").event_id.count().reindex(order).fillna(0)
    a,b=st.columns(2)
    with a:
        st.markdown('<div class="card"><b>Event Volume</b>',unsafe_allow_html=True)
        st.bar_chart(funnel,height=350)
        st.markdown("</div>",unsafe_allow_html=True)
    with b:
        st.markdown('<div class="card"><b>Stage Conversion</b>',unsafe_allow_html=True)
        for i in range(3):
            rate=100*funnel.iloc[i+1]/funnel.iloc[i] if funnel.iloc[i] else 0
            st.metric(f"{order[i]} → {order[i+1]}",f"{rate:.1f}%")
        st.markdown(f'<div class="insight"><b>View → Purchase event rate:</b> {event_conversion:.2f}%. This is an event-level diagnostic, not a user-level conversion rate.</div>',unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)
    st.info("Product decision: high traffic with weak purchase activity is a reason to investigate price, reviews, availability, product-page quality and checkout friction.")

with tab3:
    st.subheader("Customer Retention")
    st.caption("Measure whether customers return after their first delivered order.")
    if len(customer_orders):
        dist=customer_orders.value_counts().sort_index()
        a,b=st.columns(2)
        with a:
            st.markdown('<div class="card"><b>Orders per Customer</b>',unsafe_allow_html=True)
            st.bar_chart(dist,height=320)
            st.markdown("</div>",unsafe_allow_html=True)
        with b:
            st.markdown('<div class="card"><b>Customer Mix</b>',unsafe_allow_html=True)
            st.metric("Repeat customers",f"{int(customer_orders.ge(2).sum()):,}")
            st.metric("One-time customers",f"{int(customer_orders.eq(1).sum()):,}")
            st.metric("Repeat purchase rate",f"{repeat_rate:.1f}%")
            st.markdown('<div class="insight"><b>Product question:</b> What can increase the probability that a first-time buyer returns?</div>',unsafe_allow_html=True)
            st.markdown("</div>",unsafe_allow_html=True)

with tab4:
    st.subheader("Product Opportunity Analysis")
    st.caption("Prioritize products using traffic and purchase behavior.")
    pf=fe.pivot_table(index="product_id",columns="event_type",values="event_id",aggfunc="count",fill_value=0).reset_index()
    for c in ["Viewed Product","Purchased"]:
        if c not in pf.columns: pf[c]=0
    pf["view_to_purchase_pct"]=100*pf["Purchased"]/pf["Viewed Product"].replace(0,1)
    opp=pf.merge(products,on="product_id").sort_values(["Viewed Product","view_to_purchase_pct"],ascending=[False,True])
    st.markdown('<div class="card"><b>🔎 High-Traffic / Low-Conversion Candidates</b>',unsafe_allow_html=True)
    st.dataframe(opp[["product_id","product_name","category","Viewed Product","Purchased","view_to_purchase_pct"]].head(15),use_container_width=True,hide_index=True)
    st.markdown("</div>",unsafe_allow_html=True)
    a,b=st.columns(2)
    with a:
        st.markdown('<div class="card"><b>Traffic vs Purchases</b>',unsafe_allow_html=True)
        st.bar_chart(opp.set_index("product_name")[["Viewed Product","Purchased"]].head(10),height=320)
        st.markdown("</div>",unsafe_allow_html=True)
    with b:
        st.markdown('<div class="card"><b>💡 Product Recommendations</b>',unsafe_allow_html=True)
        for title,body in [
            ("Investigate high-traffic / low-conversion products","Review price, ratings, availability, images and product-page quality."),
            ("Improve repeat purchasing","Test post-purchase recommendations, replenishment reminders or loyalty nudges."),
            ("Protect strong categories","Compare conversion and retention before increasing promotional spend."),
            ("Improve instrumentation","Track user sessions so future analysis can calculate true user-level funnel conversion.")
        ]:
            st.markdown(f'<div class="recommendation"><div class="title">{title}</div><div class="body">{body}</div></div>',unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)

with tab5:
    st.subheader("Data Explorer")
    st.caption("The dashboard is backed by real CSV tables included in the project.")
    choice=st.selectbox("Choose dataset",["Orders","Products","Customers","Events"])
    data={"Orders":fo,"Products":products[products.product_id.isin(allowed_products)],"Customers":customers,"Events":fe}[choice]
    st.write(f"**{len(data):,} rows**")
    st.dataframe(data.head(500),use_container_width=True,hide_index=True)
    st.download_button("⬇️ Download current table",data.to_csv(index=False).encode(),f"{choice.lower()}_filtered.csv","text/csv")

st.markdown("---")
st.caption("Portfolio project • Synthetic data • Product analytics practice")
