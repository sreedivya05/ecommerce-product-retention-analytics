import pandas as pd
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
customers=pd.read_csv(BASE/'data/customers.csv')
products=pd.read_csv(BASE/'data/products.csv')
orders=pd.read_csv(BASE/'data/orders.csv')
events=pd.read_csv(BASE/'data/events.csv')
d=orders[orders.status=='Delivered'].copy()
print('Customers:',customers.customer_id.nunique())
print('Orders:',orders.order_id.nunique())
print('Delivered revenue:',round(d.revenue.sum(),2))
print('AOV:',round(d.revenue.sum()/d.order_id.nunique(),2))
views=(events.event_type=='Viewed Product').sum()
purchases=(events.event_type=='Purchased').sum()
print('View-to-purchase event rate:',round(100*purchases/views,2),'%')
co=d.groupby('customer_id').order_id.nunique()
print('Repeat purchase rate:',round(100*co.ge(2).mean(),2),'%')
print(d.merge(products,on='product_id').groupby('category').revenue.sum().sort_values(ascending=False))
