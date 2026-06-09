import os
import psycopg2

DATABASE_URL = 'postgresql://citizenhub_user:vDBiYO2MgMT4IJ1cwXwxnG5YHKZI6u8g@dpg-d8faho8g4nts738o6k3g-a.virginia-postgres.render.com/citizenhub_qyqx'

try:
    conn = psycopg2.connect(DATABASE_URL)
    print('Connection successful!')
    conn.close()
except Exception as e:
    print(f'Connection failed: {e}')
