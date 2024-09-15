from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def get_all_Years():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct Year(s.`datetime`) as year
                        from sighting s 
                        order by s.`datetime` desc """
            cursor.execute(query)

            for row in cursor:
                result.append(row["year"])
            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def get_all_shapes(anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct s.shape 
                        from sighting s 
                        where s.shape != "unknown" 
                        and s.shape !=""
                        and year(s.`datetime`) =%s
                        order by s.shape asc """
            cursor.execute(query, (anno,))

            for row in cursor:
                result.append(row["shape"])
            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def getNodes(anno,forma):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select *
                        from sighting s 
                        where year(s.`datetime`)=%s
                        and s.shape = %s """
            cursor.execute(query, (anno,forma,))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result



    @staticmethod
    def get_all_edges(anno, forma, idMap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select t1.id as id1, abs(t1.longitude) as l1, t2.id as id2, abs(t2.longitude) as d2
                    from (select * from sighting s where YEAR(`datetime`) = %s and shape = %s) t1 ,
                    (select * from sighting s where YEAR(`datetime`) = %s and shape = %s) t2
                    where t1.state = t2.state and abs(t1.longitude) < abs(t2.longitude)
                    order by t1.longitude, t2.longitude"""
            cursor.execute(query, (anno, forma, anno, forma))

            for row in cursor:
                result.append((idMap[row['id1']], idMap[row['id2']]))
            cursor.close()
            cnx.close()
        return result