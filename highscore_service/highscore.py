import socket
import pymysql
import time

HOST, PORT = "localhost", 6000
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))
s.setblocking(0)

print("Server running...")

# Saves the score to db.
def saveHighScore(level, name, score):
    # Connect to db.
    conn = pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           passwd='root',
                           db='blender')
    cursor = conn.cursor()
    # SQL query.
    sqlLvl1 = "INSERT INTO Level1 (name, score) VALUES (%s, %s)"
    sqlLvl2 = "INSERT INTO Level2 (name, score) VALUES (%s, %s)"
    if level == 'Level1':
        cursor.execute(sqlLvl1, (str(name), int(score)))
    elif level == 'Level2':
        cursor.execute(sqlLvl2, (str(name), int(score)))
    conn.commit()
    print("\nAt "+ str(time.ctime()) +" Inserted: " + name + " " + str(score) +" into " + level)
    conn.close()

# Sends a list of the top 10 scores to addr.
def sendHighScore(client, db):
    # Connect to db.
    conn = pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           passwd='root',
                           db='blender')
    cursor = conn.cursor()
    # SQL query.
    sql = ("SELECT name, score FROM %s order by score DESC LIMIT 10;"% (db))
    cursor.execute(sql)
    result = cursor.fetchall()
    # send results back
    s.sendto(str(result).encode('utf-8'), client)
    print("\nAt "+ str(time.ctime()) +" Send: %s | to | %s" % (str(result), client))
    conn.close()

while True:
    try:
        # Recive data and print it.
        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        print("\nAt "+ str(time.ctime()) +" Received: " + data + " from " + str(addr))
        #If the first word == score it saves the score.
        if data.split(None, 1)[0] == "score":
            saveHighScore(data.split()[1], data.split()[2], data.split()[3])

        # If the first word == list it sends the top 10.
        elif data.split(None, 1)[0] == "list":
            sendHighScore(addr, data.split()[1])

    except:
        pass

s.close()
