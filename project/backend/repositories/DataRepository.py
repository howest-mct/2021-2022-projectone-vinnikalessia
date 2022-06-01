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
    def create_historiek_joy(deviceid, commentaar, waarde = 1, actieid = 1):
    # def create_historiek_joy_1_x(waarde, commentaar = "joystick 1 registreerde beweging op x-as"):
        sql = "INSERT INTO historiek(deviceid, actieid, waarde, commentaar, actiedatum) VALUE(%s, %s, %s, %s, %s)"
        params = [deviceid, actieid, waarde, commentaar, datetime.datetime.now()]
        result = Database.execute_sql(sql, params)
        print("history created")
        return result

    # # todo    
    @staticmethod
    def update_status_lamp(x_as, y_as):
        sql = "UPDATE  SET status = %s WHERE id = %s"
        params = []
        return Database.execute_sql(sql, params)

    # @staticmethod
    # def update_status_alle_lampen(status):
    #     sql = "UPDATE lampen SET status = %s"
    #     params = [status]
    #     return Database.execute_sql(sql, params)
