from .Database import Database
import datetime


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def read_spellen():
        sql = "SELECT * from spel"
        return Database.get_rows(sql)

    @staticmethod
    def read_devices():
        sql = "SELECT * from device"
        return Database.get_rows(sql)

    @staticmethod
    def read_device_by_id(id):
        sql = "SELECT * from device WHERE deviceid = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    @staticmethod
    def read_alle_spelers():
        sql = "SELECT * from player"
        return Database.get_rows(sql)
    
    @staticmethod
    def read_speler_by_id(id):
        sql = "SELECT * from player WHERE playerid = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    @staticmethod
    def read_alle_waarden():
        sql = "SELECT * from historiek"
        return Database.get_rows(sql)

    @staticmethod
    def create_historiek(deviceid, commentaar, waarde = 1, actieid = 1):
        sql = "INSERT INTO historiek(deviceid, actieid, waarde, commentaar, actiedatum) VALUE(%s, %s, %s, %s, %s)"
        params = [deviceid, actieid, waarde, commentaar, datetime.datetime.now()]
        result = Database.execute_sql(sql, params)
        print(result)
        return result

    @staticmethod
    def create_game(winnaar, verliezer):
        sql = "insert into spel(winnerid, verliezerid, datum) value(%s, %s, %s)"
        params = [winnaar, verliezer, datetime.datetime.now()]
        result = Database.execute_sql(sql, params)
        return result

    
        