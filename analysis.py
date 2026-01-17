import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data/cleaned_complaints.csv')

# Complaints by Product
plt.figure(figsize=(10,6))
sns.countplot(y='Product', data=df, order=df['Product'].value_counts().index)
plt.title('Complaints by Product')
plt.savefig('visuals/product_bar.png', bbox_inches='tight')

# Complaints by Issue
plt.figure(figsize=(10,6))
sns.countplot(y='Issue', data=df, order=df['Issue'].value_counts().index[:15])
plt.title('Top 15 Issues')
plt.savefig('visuals/issue_bar.png', bbox_inches='tight')

# Complaints over time
df['Date received'] = pd.to_datetime(df['Date received'])
df.set_index('Date received', inplace=True)
monthly_counts = df.resample('M').size()
plt.figure(figsize=(12,6))
monthly_counts.plot()
plt.title('Monthly Complaints Over Time')
plt.savefig('visuals/complaints_over_time.png', bbox_inches='tight')
