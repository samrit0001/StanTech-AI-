import pandas as pd
import numpy as np
from db_connection import product_collection

df = pd.read_csv('products.csv')

df['price'].fillna(df['price'].median(), inplace=True)
df['quantity_sold'].fillna(df['quantity_sold'].median(), inplace=True)

category_avg_rating = df.groupby('category')['rating'].mean()
df['rating'] = df.apply(lambda row: category_avg_rating[row['category']] if np.isnan(row['rating']) else row['rating'], axis=1)

# Ensure numeric fields
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['quantity_sold'] = pd.to_numeric(df['quantity_sold'], errors='coerce')
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

# Upload cleaned data to MongoDB
product_collection.delete_many({})
product_collection.insert_many(df.to_dict(orient='records'))

# Create summary report
summary_df = df.groupby('category').apply(
    lambda x: pd.Series({
        'total_revenue': (x['price'] * x['quantity_sold']).sum(),
        'top_product': x.loc[x['quantity_sold'].idxmax()]['product_name'],
        'top_product_quantity_sold': x['quantity_sold'].max()
    })
).reset_index()

# Save summary to CSV
summary_df.to_csv('summary_report.csv', index=False)
