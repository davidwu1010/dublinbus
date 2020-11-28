from sqlalchemy import create_engine
from sqlalchemy import exc
import re

password = ''
engine = create_engine(f'mysql+pymysql://dublinbus:{password}@localhost/gtfs')
connection = engine.connect()
transaction = connection.begin()

try:
    result = connection.execute('SELECT StopID FROM Stops')
    stop_ids = map(lambda row: row['StopID'], result)

    for stop_id in stop_ids:
        stop_number = re.sub(r'^....DB0*', '', stop_id)
        print(stop_number)
        connection.execute(f"UPDATE Stops SET StopNumber = {stop_number}"
                           f" WHERE StopID = '{stop_id}'")

    transaction.commit()
    print('Done')
except exc.SQLAlchemyError as e:
    print(e)
    transaction.rollback()
