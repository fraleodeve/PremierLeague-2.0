from database.DB_connect import DBConnect
from model.arco import Arco
from model.giocatore import Giocatore
from model.media import Media


class DAO():

    @staticmethod
    def getAllGiocatori():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select *
                    from players"""
        cursor.execute(query)

        res = []

        for row in cursor:
            res.append(Giocatore(**row))

        cursor.close()
        conn.close()

        return res

    @staticmethod
    def getMedia(goal):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select t.PlayerID, (t.goal/t.partite) as peso
                        from (select a.PlayerID, sum(a.Goals) as goal, count(*) as partite
                        from actions a 
                        group by a.PlayerID ) t
                        having peso > %s"""
        cursor.execute(query, (goal,))

        res = []

        for row in cursor:
            res.append(Media(**row))

        cursor.close()
        conn.close()

        return res

    @staticmethod
    def getEdges(goal):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select b1.PlayerID as p1, b2.PlayerID as p2, (b1.TimePlayed - b2.TimePlayed) as minuti
                    from (select c.PlayerID, a.MatchID, a.TeamID, a.TimePlayed
                    from (select t.PlayerID, (t.goal/t.partite) as peso
                            from (select a.PlayerID, sum(a.Goals) as goal, count(*) as partite
                            from actions a 
                            group by a.PlayerID ) t
                            having peso > %s) c, actions a 
                    where a.PlayerId = c.PlayerID and a.starts = 1
                    order by a.matchID) b1,
                    (select c.PlayerID, a.MatchID, a.TeamID, a.TimePlayed
                    from (select t.PlayerID, (t.goal/t.partite) as peso
                            from (select a.PlayerID, sum(a.Goals) as goal, count(*) as partite
                            from actions a 
                            group by a.PlayerID ) t
                            having peso > %s) c, actions a 
                    where a.PlayerId = c.PlayerID and a.starts = 1
                    order by a.matchID) b2
                    where b1.MatchID = b2.MatchID and b1.PlayerID <> b2.PlayerID and b1.TeamID <> b2.TeamID and b1.PlayerID < b2.PlayerID and b1.TimePlayed <> b2.TImePlayed
                    order by b1.MatchID"""
        cursor.execute(query, (goal, goal))

        res = []

        for row in cursor:
            res.append(Arco(**row))

        cursor.close()
        conn.close()

        return res