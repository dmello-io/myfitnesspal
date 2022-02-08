import os
import myfitnesspal
import datetime
from datetime import date
import mysql.connector as database

sql_username = os.environ.get("pysql_username")
sql_password = os.environ.get("pysql_password")
mfp_username = os.environ.get("mfp_username")
mfp_password = os.environ.get("mfp_password")


def main():
    client = myfitnesspal.Client(mfp_username, password=mfp_password)
    days = 3

    for i in range(days):
        today = date.today() - datetime.timedelta(days=i)
        print(today)
        data = get_entries(client, today)
        insert_data(data)


def insert_data(data):
    connection = database.connect(
        user=sql_username,
        password=sql_password,
        host="tofu",
        port=3306,
        database="MyFitnessPal"
    )

    cursor = connection.cursor()

    meals = data.meals
    for meal in meals:
        for entry in meal:
            print(data.date, meal.name, "\t", entry)
            split_name = entry.name.split(",")

            name = ','.join(split_name[:-1])
            portion = split_name[-1]

            split_portion = portion.split(" ")
            portion = split_portion[1]
            unit = ' '.join(split_portion[2:])

            statement = "INSERT INTO food(item_date, meal, item_name, serving, unit, calories, carbohydrates, fat, protein, sodium, sugar) \
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) \
                         ON DUPLICATE KEY UPDATE serving=%s, unit=%s, calories=%s, carbohydrates=%s, fat=%s, protein=%s, sodium=%s, sugar=%s"

            values = (
                data.date.strftime('%Y-%m-%d'),         # item_date
                meal.name,                              # meal
                name[0:250],                            # item_name
                portion,                                # portion
                unit,                                   # unit
                entry['calories'],                      # calories
                entry['carbohydrates'],                 # carbohydrates
                entry['fat'],                           # fat
                entry['protein'],                       # protein
                entry['sodium'],                        # sodium
                entry['sugar'],                         # sugar
                portion,                                # portion
                unit,                                   # unit
                entry['calories'],                      # calories
                entry['carbohydrates'],                 # carbohydrates
                entry['fat'],                           # fat
                entry['protein'],                       # protein
                entry['sodium'],                        # sodium
                entry['sugar'],                         # sugar
            )

            cursor.execute(statement, values)
            connection.commit()


def get_entries(client, for_date):
    YYYY = for_date.year
    M = for_date.month
    D = for_date.day

    data = client.get_date(YYYY, M, D)

    return data


if __name__ == "__main__":
    main()
