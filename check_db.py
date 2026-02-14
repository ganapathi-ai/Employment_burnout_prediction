import sqlite3

conn = sqlite3.connect('user_requests.db')
cursor = conn.cursor()

# Get table schema
cursor.execute('PRAGMA table_info(user_requests)')
cols = cursor.fetchall()

print('Database Columns:')
for col in cols:
    print(f'  {col[1]} ({col[2]})')

# Get data
cursor.execute('SELECT * FROM user_requests')
rows = cursor.fetchall()

print(f'\nTotal records: {len(rows)}')
if rows:
    print('\nFirst record:')
    for i, col in enumerate(cols):
        print(f'  {col[1]}: {rows[0][i]}')

conn.close()
