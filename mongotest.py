import os
import psycopg2

conn = psycopg2.connect(dbname="ddcdvtofrshbnj", user="ntvhhmrhgzdmqh", password="70f5719386ca8d7a4464e7ba903ff81ddbe1fe1d444071cc5ce4e1ad28059870",
                        host="ec2-54-247-89-181.eu-west-1.compute.amazonaws.com", port="5432")

cur = conn.cursor()


def execute_command(command):
    try:
        cur.execute(command)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


execute_command("SELECT * FROM data")
rows = cur.fetchall()

for row in rows:
    print("Row: ")
    print(str(row))
    print("ID: " + str(row[0]))
    print("URL: " + str(row[1]))
    print("Points: " + str(row[2]))
    print("Type: " + str(type(row)))
    print("\n")
