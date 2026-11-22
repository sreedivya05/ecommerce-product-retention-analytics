import pandas as pd
import streamlit as st
from pathlib import Path
st.set_page_config(page_title='Sales BI Analytics',page_icon='📈',layout='wide')
BASE=Path(__file__).parent
sales=pd.read_csv(BASE/'data/sales.csv',parse_dates=['order_date'])
products=pd.read_csv(BASE/'data/products.csv')
customers=pd.read_csv(BASE/'data/customers.csv')
salespersons=pd.read_csv(BASE/'data/salespersons.csv')
st.markdown('''<style>
.stApp{background:#f7f9fc}.block-container{max-width:1400px;padding-top:2rem}
.hero{background:linear-gradient(135deg,#111827,#1e3a5f);padding:30px 35px;border-radius:18px;color:white;margin-bottom:22px}
.hero h1{margin:0;font-size:32px}.hero p{color:#cbd5e1}
.kpi{background:white;border:1px solid #e2e8f0;border-radius:14px;padding:18px;min-height:105px}
.kpi-label{font-size:11px;color:#64748b;font-weight:700;text-transform:uppercase}
.kpi-value{font-size:25px;font-weight:800;color:#0f172a;margin-top:6px}
.insight{background:#eff6ff;border-left:4px solid #2563eb;padding:14px 18px;border-radius:8px;margin-top:12px}
</style>''',unsafe_allow_html=True)
st.markdown('''<div class="hero"><h1>📈 Sales Performance & Business Intelligence</h1>
<p>Revenue, profitability, regional, product and salesperson analysis.</p></div>''',unsafe_allow_html=True)
total=sales.sales.sum(); profit=sales.profit.sum(); margin=100*profit/total
orders=sales.order_id.nunique(); aov=total/orders
cols=st.columns(5)
for c,label,val in zip(cols,['Total Sales','Profit','Profit Margin','Orders','AOV'],
                       [f'₹{total/100000:.2f}L',f'₹{profit/100000:.2f}L',f'{margin:.1f}%',f'{orders:,}',f'₹{aov:,.0f}']):
    c.markdown(f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-value">{val}</div></div>',unsafe_allow_html=True)
st.subheader('Monthly Sales & Profit')
st.line_chart(sales.set_index('order_date').resample('ME')[['sales','profit']].sum())
a,b=st.columns(2)
with a:
    st.subheader('Regional Sales')
    regional=sales.groupby('region').agg(sales=('sales','sum'),profit=('profit','sum'))
    regional['margin_pct']=100*regional.profit/regional.sales
    st.bar_chart(regional.sales.sort_values(ascending=False))
    st.dataframe(regional.sort_values('sales',ascending=False),use_container_width=True)
with b:
    st.subheader('Category Profit')
    category=sales.merge(products,on='product_id').groupby('category').agg(sales=('sales','sum'),profit=('profit','sum')).sort_values('profit',ascending=False)
    st.bar_chart(category.profit)
    st.dataframe(category,use_container_width=True)
st.subheader('Product Profitability')
product=sales.merge(products,on='product_id').groupby(['product_id','product_name','category']).agg(sales=('sales','sum'),profit=('profit','sum'),units=('quantity','sum'))
product['margin_pct']=100*product.profit/product.sales
st.dataframe(product.sort_values('profit',ascending=False).head(15),use_container_width=True)
st.subheader('Salesperson Leaderboard')
rep=sales.merge(salespersons,on='salesperson_id').groupby(['salesperson_id','salesperson_name','team','region']).agg(sales=('sales','sum'),profit=('profit','sum'),orders=('order_id','nunique'))
rep['margin_pct']=100*rep.profit/rep.sales
st.dataframe(rep.sort_values('sales',ascending=False).head(15),use_container_width=True)
lr=regional.margin_pct.idxmin(); hr=regional.sales.idxmax(); lp=product.margin_pct.idxmin()
st.subheader('Business Insights')
st.markdown(f'''<div class="insight"><b>Revenue leader:</b> {hr} has the highest sales. Compare its growth and margin before allocating more resources.</div>
<div class="insight"><b>Margin watch:</b> {lr} has the lowest regional margin. Review discounting, product mix and costs.</div>
<div class="insight"><b>Product watch:</b> {lp} has the lowest product margin. Investigate pricing, discount and cost structure.</div>''',unsafe_allow_html=True)
