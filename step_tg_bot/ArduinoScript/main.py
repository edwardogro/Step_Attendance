import serial
import time
from datetime import datetime
import connect_to_db as con

count = 0
while not con.connect_to_db():
    time.sleep(1)
    count += 1
    print(f'Попытка переподключения - {count}')

time_arrival = con.db.test
record = con.db.eml_test
pos_empl = con.db.position_test

# Функция для записи времени прихиода и ухода сотрудника в бд
def update_time_in_db(emloyee_id, field_in_bd, arrival_or_leaving_time, status, current_date):
    record.update_one({'_id': emloyee_id}, {'$set':
            {field_in_bd: arrival_or_leaving_time, 
            'status': status,
            'current_date': current_date
            }})

ser = serial.Serial("COM4")
print(ser.name)

while True:
    inp = str(ser.read())[2]
    if inp:
        uid = ''
        uid += inp
        for i in range(27):
            uid += str(ser.read())[2]
        uid = uid[uid.find("UID:"):uid.find("\\\\Card SAK")]
        uid = uid[5:]
        # Если сотрудник есть в базе, то обновляем его данные
        if record.count_documents({"uid":uid}) == 1:
            empl = record.find_one({"uid":uid})
            current_date = datetime.today().strftime("%d.%m.%Y")
            today_time = datetime.today().strftime("%H:%M")
            field_in_bd = ''
            if empl['status'] == False:
                field_in_bd = 'arrival_time'
                update_time_in_db(empl['_id'], field_in_bd, today_time, True, current_date)
                print('Сотрудник {} пришел в {}'.format(empl['fullname'], today_time))
            else:
                field_in_bd = 'leaving_time'
                update_time_in_db(empl['_id'], field_in_bd, today_time, False, current_date)
                print('Сотрудник {} ушел в {}'.format(empl['fullname'], today_time))
        # Иначе сообщаем
        else:
            print('Данного сотрудника нет в базе данных')


