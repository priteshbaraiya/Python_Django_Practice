import os
import django
import pandas as pd
from django.db import connection  # <--- Step 1: Connection import kiya

# Step 2: Project Settings setup (Project name 'hello' hai)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hello.settings')
django.setup()

# Step 3: App Models Import ('inventory' app se)
from inventory.models import Product, Sale

def load_data():
    # Step 4: Database connection ko force open karna (Fix for NoneType error)
    print("Connecting to Database...")
    connection.ensure_connection()

    # ---------------------------------------------------------
    # 1. Load Inventory (Product) Data
    # ---------------------------------------------------------
    print("Loading Inventory Data...")
    try:
        # Note: Agar file ka naam 'retail_store_clean_2.csv' hai to yaha change karein
        df_inv = pd.read_csv('retail_store_clean_2.csv') 
        
        products_to_create = []
        for index, row in df_inv.iterrows():
            products_to_create.append(Product(
                product_id=row['Product ID'],
                category=row['Category'],
                inventory_level=row['Inventory Level']
            ))
        
        # Step 5: batch_size add kiya taki database hang na ho
        Product.objects.bulk_create(products_to_create, batch_size=500, ignore_conflicts=True)
        print(f"✅ {len(products_to_create)} Products added successfully!")
        
    except FileNotFoundError:
        print("❌ Error: 'clean_inventory_data.csv' file nahi mili! File name check karo.")
    except Exception as e:
        print(f"❌ Error in Inventory: {e}")

    # ---------------------------------------------------------
    # 2. Load Sales Data
    # ---------------------------------------------------------
    print("Loading Sales Data...")
    try:
        # Note: Agar file ka naam 'retail_sales_clean_2.csv' hai to yaha change karein
        df_sales = pd.read_csv('retail_sales_clean_2.csv')
        df_sales['Date'] = pd.to_datetime(df_sales['Date']) # Date format fix

        sales_to_create = []
        for index, row in df_sales.iterrows():
            sales_to_create.append(Sale(
                transaction_id=row['Transaction ID'],
                date=row['Date'],
                product_category=row['Product Category'],
                quantity=row['Quantity'],
                total_amount=row['Total Amount']
            ))
        
        # Step 5: batch_size add kiya
        Sale.objects.bulk_create(sales_to_create, batch_size=500, ignore_conflicts=True)
        print(f"✅ {len(sales_to_create)} Sales records added successfully!")
        
    except FileNotFoundError:
        print("❌ Error: 'clean_sales_data.csv' file nahi mili! File name check karo.")
    except Exception as e:
        print(f"❌ Error in Sales: {e}")

if __name__ == '__main__':
    load_data()