# Supply Chain Data Warehouse & BI Pipeline

A complete end-to-end Business Intelligence pipeline built on the Microsoft BI stack, using the DataCo Smart Supply Chain dataset (~180,000 transactional records, 2015–2018).

## Project Overview

This project demonstrates a full traditional ETL/BI pipeline:

**Raw Data → Staging → Data Warehouse → SSAS Tabular Model → Power BI Dashboard**

The goal is to analyze supply chain performance, focusing on delivery efficiency, sales trends, and profitability across regions, products, and shipping modes.

---

## Dataset Source

The raw dataset used in this project is the **DataCo Smart Supply Chain Dataset** available on Kaggle:

🔗 [Download Dataset from Kaggle](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis)

Download `DataCoSupplyChainDataset.csv` and place it in:
`C:\Users\ACER\Downloads\DataCoSupplyChainDataset.csv`

Then run the Python scripts to generate the required source files before executing the SSIS packages.

---

## Dataset Details

- **Source:** DataCo Smart Supply Chain Dataset (Kaggle)
- **Records:** ~180,519 order line items
- **Period:** 2015–2018
- **Domain:** Global supply chain and order management

---

## Tech Stack

| Layer | Technology |
|---|---|
| Database | SQL Server 2019 |
| ETL | SQL Server Integration Services (SSIS) |
| Data Warehouse | SQL Server 2019 |
| Semantic Model | SQL Server Analysis Services (SSAS) Tabular |
| Reporting | Power BI Desktop |
| Data Prep | Python (pandas, SQLAlchemy, pyodbc) |

---

## Architecture

```
DataCo CSV Dataset (Kaggle)
        ↓
Python Data Preparation Scripts
        ↓
Staging Layer (SupplyChainStaging)
   - StgOrders
   - StgCustomer
   - StgProduct
   - StgGeography
        ↓
Data Warehouse (SupplyChainDW)
   - DimDate
   - DimCustomer (SCD Type 2)
   - DimProduct
   - DimGeography
   - DimShipper
   - FactOrderItem (180,519 rows)
        ↓
SSAS Tabular Model (SupplyChain_SSAS)
   - 7 DAX Measures
   - 3 Hierarchies
   - 1 KPI
        ↓
Power BI Dashboard (3 pages)
```

---

## Repository Structure

```
supply-chain-data-warehouse/
│
├── SC_Load_Staging.dtsx          # SSIS package - Load staging layer
├── SC_Load_DW.dtsx               # SSIS package - Load data warehouse
├── SC_Accumulating_Fact.dtsx     # SSIS package - Update accumulating fact
│
├── Model.bim                     # SSAS Tabular model definition
├── SupplyChain_Report.pbix       # Power BI report (3 pages)
│
├── fix_orders.py                 # Python script - Add geography columns to orders
├── reload_orders.py              # Python script - Reload orders into SQL Server
│
└── README.md
```

---

## SSIS Packages

| Package | Description |
|---|---|
| `SC_Load_Staging.dtsx` | Loads raw CSV and SQL data into staging tables. Truncates and reloads on each run. |
| `SC_Load_DW.dtsx` | Transforms and loads staging data into DW dimensions and fact table using surrogate key lookups and a stored procedure. |
| `SC_Accumulating_Fact.dtsx` | Updates accumulating fact columns tracking the order lifecycle from creation to shipment. |

---

## Data Warehouse Design

### Dimensions

| Table | Description | Notes |
|---|---|---|
| DimDate | Date dimension | Year, Quarter, Month, Day |
| DimCustomer | Customer details | SCD Type 2 — tracks historical changes |
| DimProduct | Product, Category, Department | 118 products |
| DimGeography | Market, Region, Country, State, City | 3,716 locations |
| DimShipper | Shipping mode and delivery status | 12 combinations |

### Fact Table

**FactOrderItem** — 180,519 rows

| Column | Description |
|---|---|
| OrderItemKey | Surrogate key |
| DateKey, CustomerKey, ProductKey, GeographyKey, ShipperKey | Foreign keys to dimensions |
| Sales | Order item sales amount |
| OrderItemTotal | Total order item value |
| OrderProfitPerOrder | Profit per order |
| BenefitPerOrder | Benefit per order |
| OrderItemDiscount | Discount amount |
| OrderItemDiscountRate | Discount rate |
| OrderItemQuantity | Quantity ordered |
| OrderItemProfitRatio | Profit ratio |
| DaysShippingReal | Actual shipping days |
| DaysShipmentScheduled | Scheduled shipping days |
| LateDeliveryRisk | Binary flag for late delivery risk |
| accm_txn_create_time | Order date (accumulating fact) |
| accm_txn_complete_time | Shipping date (accumulating fact) |
| txn_process_time_hours | Hours from order to shipment |

---

## SSAS Tabular Model

### DAX Measures

| Measure | Formula |
|---|---|
| Total Sales | `SUM(FactOrderItem[Sales])` |
| Total Profit | `SUM(FactOrderItem[OrderProfitPerOrder])` |
| Total Orders | `DISTINCTCOUNT(FactOrderItem[OrderId])` |
| Total Quantity | `SUM(FactOrderItem[OrderItemQuantity])` |
| Avg Shipping Days | `AVERAGE(FactOrderItem[DaysShippingReal])` |
| Late Delivery Count | `CALCULATE(COUNTROWS(FactOrderItem), FactOrderItem[LateDeliveryRisk]=1)` |
| Late Delivery % | `DIVIDE([Late Delivery Count],[Total Orders],0)*100` |

### Hierarchies

| Hierarchy | Levels |
|---|---|
| Product Hierarchy | Department → Category → Product |
| Geography Hierarchy | Market → Region → Country → State → City |
| Date Hierarchy | Year → Quarter → Month → Day |

### KPI
- **Late Delivery % KPI** with traffic light status indicators (target: 50%)

---

## Power BI Report

3-page interactive dashboard connected via **live connection** to SSAS Tabular model.

### Page 1 — Overview Dashboard
- KPI Cards: Total Sales (36.78M), Total Profit (3.97M), Total Orders (65.7K)
- Total Sales by Department (bar chart)
- Total Profit by Region (bar chart)
- Late Delivery % by Shipping Mode (bar chart)
- Total Orders by Year (bar chart)
- Slicers: Year, Shipping Mode

### Page 2 — Detailed Analysis
- Drill-down matrix: Department → Category → Product with Total Sales and Total Profit
- Sales trend line chart by Year
- Avg Shipping Days by Shipping Mode (bar chart)
- Slicer: Year

### Page 3 — Delivery Performance
- Late Delivery % KPI card (150.53% overall)
- Late Delivery Count by Region (bar chart)
- Order Status breakdown by DeliveryStatus (donut chart)
- Late Delivery % by Department (bar chart)
- Slicer: Year

---

## Python Scripts

| Script | Description |
|---|---|
| `fix_orders.py` | Reads the raw Kaggle CSV and extracts orders with geography columns (Order City, Order Country, Order Region) added. Saves to `orders.csv`. |
| `reload_orders.py` | Reloads the Orders table in SQL Server `SupplyChainDB` with the updated schema including geography columns. |

---

## How to Run

### Prerequisites
- SQL Server 2019
- SQL Server Analysis Services 2019 (Tabular mode instance)
- Visual Studio 2022 with SSIS/SSAS extensions
- Power BI Desktop
- Python 3.x with pandas, sqlalchemy, pyodbc

### Steps

1. Download the dataset from Kaggle and place it at:
   `C:\Users\ACER\Downloads\DataCoSupplyChainDataset.csv`

2. Run the Python data preparation scripts:
   ```
   python fix_orders.py
   python reload_orders.py
   ```

3. Create the databases `SupplyChainStaging` and `SupplyChainDW` in SQL Server.

4. Open the SSIS project in Visual Studio 2022 and execute packages in order:
   - `SC_Load_Staging.dtsx`
   - `SC_Load_DW.dtsx`
   - `SC_Accumulating_Fact.dtsx`

5. Deploy `Model.bim` to your SSAS Tabular instance.

6. Open `SupplyChain_Report.pbix` in Power BI Desktop and connect to your SSAS instance.

---

## Key Findings

- **Fan Shop** is the highest revenue department (~$17M in total sales)
- **54.82%** of orders experienced late delivery — a significant operational issue
- **Central America** and **Western Europe** have the highest late delivery counts
- **Standard Class** shipping has the most late deliveries
- Sales are consistent across 2015–2017, with 2018 being a partial year
- Average shipping time varies significantly by shipping mode

---

## Author

**Wethmi** — Built as a deep-dive learning project to master the Microsoft BI stack end-to-end.
