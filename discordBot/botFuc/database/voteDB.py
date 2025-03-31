import sqlite3

con = sqlite3.connect('./Database.db')

cur = con.cursor()

# DropTable
#
# vote
# cur.execute("DROP table if exists voteList")
# cur.execute("DROP table if exists votingItem")
# cur.execute("DROP table if exists voteStatus")

# createTable
cur.execute("CREATE TABLE if not exists voteList(serverID text, userID text, voteName text, votingItems text, "
            "primary key(serverID, userID, voteName)) ;")
cur.execute("CREATE TABLE if not exists votingItem(serverID text, userID text, name text, item text, "
            "primary key(serverID, userID, name));")
cur.execute("CREATE TABLE if not exists voteStatus(serverID text, voteName text, item text, count Int, "
            "primary key(serverID, voteName, item));")


def insertVoteList(serverID, userID, voteName, voteItems):
    try:
        cur.execute("INSERT into voteList Values(?, ?, ?, ?);", (serverID, userID, voteName, voteItems))

        list = str(voteItems).split(" ")
        for item in list:
            cur.execute("INSERT into voteStatus Values(?, ?, ?, ?);", (serverID, voteName, item, 0))
        con.commit()
        return True
    except:
        return False


def selectAllVote(serverID):
    cur.execute("SELECT voteName FROM voteList WHERE serverID = ?;", (serverID,))

    list = []
    for row in cur:
        list.append(row[0])

    return list


def selectVotingItems(serverID, voteName):
    cur.execute("SELECT votingItems FROM voteList WHERE serverID=? and voteName=?;", (serverID, voteName))

    item = []
    for row in cur:
        item.append(row[0])

    voteItems = str(item[0]).split(" ")

    return voteItems


# vote
def checkVoteList(serverID, voteName):
    cur.execute("SELECT userID FROM voteList WHERE serverID=? and voteName=?;", (serverID, voteName))

    list = []
    for row in cur:
        list.append(row[0])

    if len(list) != 0:
        return True
    else:
        return False


def selectUserIDFromVote(serverID, userID, voteName):
    cur.execute("SELECT userID FROM voteList WHERE serverID=? and voteName=?;", (serverID, voteName))
    list = []
    for row in cur:
        list.append(row[0])

    if list[0] == userID:
        return True
    else:
        return False


def deleteVote(serverID, voteName):
    cur.execute("DELETE FROM voteList WHERE serverID=? and voteName=?;", (serverID, voteName))
    cur.execute("DELETE FROM votingItem WHERE serverID=? and voteName=?;", (serverID, voteName))
    cur.execute("DELETE FROM voteStatus WHERE serverID=? and voteName=?;", (serverID, voteName))
    con.commit()


def voting(serverID, userID, voteName, item):
    try:
        cur.execute("INSERT into votingItem Values(?, ?, ?, ?);", (serverID, userID, voteName, item))
        cur.execute("UPDATE voteStatus SET count = count + 1 WHERE serverID=? and voteName=? and item=?;",
                    (serverID, voteName, item))
        con.commit()
        cur.execute("SELECT count FROM voteStatus;")
        list = []
        for row in cur:
            list.append(row[0])

        print(list[0])
        return True
    except:
        return False


def status(serverID, voteName):
    cur.execute("SELECT item, count FROM voteStatus WHERE serverID=? and voteName=?;", (serverID, voteName))

    items = []
    counts = []
    for row in cur:
        items.append(row[0])
        counts.append(row[1])

    return items, counts