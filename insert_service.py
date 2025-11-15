import sqlite3

conn = sqlite3.connect("health.db")
cur = conn.cursor()

cur.execute("""
INSERT INTO services (id, name, url, expected_version, environment, enabled)
VALUES ('self-ping', 'Self Ping Service', 'http://localhost:8000/ping', NULL, 'production', 1)
""")

conn.commit()
conn.close()
print("Done.")
