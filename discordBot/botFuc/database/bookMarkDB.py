import sqlite3

con = sqlite3.connect('./Database.db')
cur = con.cursor()
# cur.execute("DROP TABLE if exists bookmark")
cur.execute("CREATE TABLE if not exists bookmark(serverID text, linkName text, link text, primary key(serverID, "
            "linkName));")


# selectLink
def selectLink(serverID, linkName):
    cur.execute("SELECT link FROM bookmark WHERE serverID=? and linkName=?;", (str(serverID), linkName))

    list = []
    for row in cur:
        list.append(row[0])

    return list


# selectAllLink
def selectAllLink(serverID):
    cur.execute("SELECT linkName, link FROM bookmark WHERE serverID=?", (str(serverID),))

    list = []
    linkList = []
    for row in cur:
        list.append(row[0])
        linkList.append(row[1])

    return list, linkList


# insertLink
def insertLink(serverID, linkName, link):
    try:
        cur.execute("INSERT into bookmark Values(?, ?, ?);", (str(serverID), linkName, link))
        con.commit()
        return True
    except:
        return False


# deleteLink
def deleteLink(serverID, linkName):
    try:
        cur.execute("DELETE FROM bookmark WHERE serverID=? and linkName=?;", (serverID, linkName))
        con.commit()

        return True
    except:
        return False


# reset bookmark(serverID)
def resetBookmark(serverID):
    try:
        cur.execute("DELETE FROM bookmark WHERE serverID=?;", (serverID,))
        con.commit()
        return True
    except:
        return False
