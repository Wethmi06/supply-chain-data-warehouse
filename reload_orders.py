import pandas as pd
import urllib
import sqlalchemy

df = pd.read_csv(r'C:\Users\ACER\Desktop\SupplyChainSources\orders.csv', encoding='latin-1')

df.columns = [
    'OrderId','OrderItemId','CustomerId','OrderDate','ShippingDate',
    'OrderStatus','DeliveryStatus','LateDeliveryRisk','ShippingMode',
    'PaymentType','OrderItemQuantity','Sales','OrderItemTotal',
    'OrderItemDiscount','OrderItemDiscountRate','OrderProfitPerOrder',
    'BenefitPerOrder','OrderItemProductPrice','OrderItemProfitRatio',
    'DaysShippingReal','DaysShipmentScheduled','ProductCardId',
    'OrderCity','OrderCountry','OrderRegion'
]

df['OrderDate'] = pd.to_datetime(df['OrderDate'])
df['ShippingDate'] = pd.to_datetime(df['ShippingDate'])

params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=.\\MSSQLSERVER2;"
    "DATABASE=SupplyChainDB;"
    "Trusted_Connection=yes;"
)
engine = sqlalchemy.create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

print("Truncating Orders table...")
with engine.connect() as conn:
    conn.execute(sqlalchemy.text("TRUNCATE TABLE Orders"))
    conn.commit()

print("Loading data...")
df.to_sql('Orders', con=engine, if_exists='append', index=False, chunksize=1000)
print(f"Done! {len(df)} rows loaded")