import pandas as pd

df = pd.read_csv(r'C:\Users\ACER\Downloads\DataCoSupplyChainDataset.csv', encoding='latin-1')

orders = df[['Order Id','Order Item Id','Customer Id',
             'order date (DateOrders)','shipping date (DateOrders)',
             'Order Status','Delivery Status','Late_delivery_risk',
             'Shipping Mode','Type',
             'Order Item Quantity','Sales','Order Item Total',
             'Order Item Discount','Order Item Discount Rate',
             'Order Profit Per Order','Benefit per order',
             'Order Item Product Price','Order Item Profit Ratio',
             'Days for shipping (real)','Days for shipment (scheduled)',
             'Order Item Cardprod Id',
             'Order City','Order Country','Order Region']]

orders.to_csv(r'C:\Users\ACER\Desktop\SupplyChainSources\orders.csv', index=False)
print('Done! Rows:', len(orders))
print('Columns:', list(orders.columns))