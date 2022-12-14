from prettytable import from_db_cursor
import sqlite3

def show_data_param(data, table):
    # Выводит таблицу table из базы данных data
    connection = sqlite3.connect(data)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM ' + table)
    mytable = from_db_cursor(cursor)
    print(mytable)
    cursor.close()
    connection.close()
    
def show_all_data_param(data='VUZ.sqlite', first = False):
    #выводит все табоицы базы дынных data, first - флаг, определяющий, будет ли использоваться таблица vuz_rf
    connection = sqlite3.connect(data)
    cursor = connection.cursor()
    cursor.execute("""\
                          SELECT name FROM sqlite_master WHERE type IN ('table','view') AND
                          name NOT LIKE 'sqlite_%' UNION ALL SELECT name FROM
                          sqlite_temp_master WHERE type IN ('table','view') ORDER BY 1;
                          """)
    ar=cursor.fetchall()
    for i in ar:
        if first:
            show_data_param(data, i[0])
        first = True
    cursor.close()
    connection.close()

def print_uniq(data = 'VUZ.sqlite',table ='vuzkart', col = ['status', 'region']):
    #выводит уникальные значения столбцов col таблицы table базы данных data
    con=sqlite3.connect(data)
    cur=con.cursor()
    data = []
    for i in col:
        sql='SELECT DISTINCT ' + i + ' FROM ' + table
        cur.execute(sql)
        uniq=cur.fetchall()
        data.append(uniq)
    cur.close()
    con.close()
    result = []
    for i in data:
        i = list(i)
        for j in range(len(i)):
          i[j] = i[j][0].replace(" ", "")
        print(i)
        result.append(i)
    return result

def selest_vuz_data(data='VUZ.sqlite', table ='vuzkart' ,columns = ['status', 'region'], values = ['Университет', 'Дальневосточный']):
    # извлечение имен ВУЗов  с соответсвующим
    #статусом и расположенных в выбранном федеральном округ (values) из таблицы table базы данных data
    connection = sqlite3.connect(data)
    cursor = connection.cursor()
    assert len(columns) == len(values)
    sql_q = "SELECT z1 AS result FROM " + table + " WHERE "
    for i in range(len(columns)):
        #добавляем дополнительные кавычки, для работы с запросом
        cur_column = "" + columns[i] + ""
        cur_value = "'" + values[i] + "%'"
        sql_q += cur_column + " LIKE " + cur_value + ' AND '
    sql_q = sql_q[:(-5)]
    #убираем последний "AND"
    cursor.execute(sql_q)
    mytable = from_db_cursor(cursor)
    #выводим значения
    print(mytable)
    cursor.close()
    connection.close()

def select_vuz(data='VUZ.sqlite', table ='vuzkart'):
    #выбор статуса выза и федерального округа и вывод соответсвующих значений из таблицы table базы данных data
    print('Выберите статус вуза и федеральный округ из списка ниже:')
    uniq = print_uniq(data)
    status = input('Статус: ')
    while status not in set(uniq[0]):
        status = input('Введите корректный статус: ')
    region = input('Федеральный округ: ')
    while region not in set(uniq[1]):
        region = input('Введите корректный округ: ')
    selest_vuz_data(values=[status, region])

def pr_stat(sotr, drop_table = True, drop_table_if_exist = False, data ='VUZ.sqlite'):
    #по введеному параметру - должности преподователя осуществляет расчёт
    #выбираем столбец/столбцы
    if sotr == 'профессор':
        dolzhnost = 'vuzstat.pr'
    elif sotr == 'доцент':
        dolzhnost = 'vuzstat.dc'
    elif sotr == 'все':
        dolzhnost = 'vuzstat.pps'
    elif sotr == 'прочие':
        dolzhnost = 'vuzstat.pps - vuzstat.dc - vuzstat.pr'
    else:
        print('Введено неверное значение!')
        return True
    connection = sqlite3.connect('VUZ.sqlite')
    cursor = connection.cursor() 
    if drop_table_if_exist:
        cursor.execute('DROP TABLE answer')
    cursor.execute('CREATE TABLE answer (person_id INTEGER PRIMARY KEY AUTOINCREMENT, region REAL NOT NULL, count_sotr REAL NOT NULL)' )
    #создаем таблицу, которая автоматически задаёт id строкам
    cursor.execute("INSERT INTO answer('region', 'count_sotr') SELECT region, SUM(res) FROM (SELECT vuzkart.region, (" + dolzhnost + ") AS res FROM vuzkart JOIN vuzstat USING(codvuz) ORDER BY vuzkart.region) GROUP BY region" )
    #добавляем основные значения
    cursor.execute("INSERT INTO answer('region', 'count_sotr') SELECT 'Все', SUM(count_sotr) FROM answer")
    #добавляем строку с итогом
    cursor.execute('SELECT *,ROUND(ROUND(count_sotr * 100) / (SELECT SUM(count_sotr)/2 FROM answer),3) AS percent FROM answer;' )
    #считаем проценты
    mytable = from_db_cursor(cursor)
    print(mytable)
    if drop_table:
        cursor.execute('DROP TABLE answer') # удаляем таблицу, если она не нужна
    connection.commit()
    cursor.close()
    connection.close()
    return False

def choice_sotr_and_stat():
    #ввод значений
    cicle = True
    while cicle:
        sotr = input('Выберете из списка должность преподавателя вузов: профессор, доцент, прочие или «Все»: ')
        cicle = pr_stat(sotr.lower())


def choice(user_answer):
    # выбор функции
    if user_answer == '1':
        show_all_data_param()
        return True
    elif user_answer == '2':
        table = input('Введите имя таблицы: ')
        while table not in  set(['vuzkart' , 'vuzstat']):
            table = input('Введите корректное имя таблицы(vuzkart, vuzstat): ')
        show_data_param('VUZ.sqlite', table)
        return True
    elif user_answer == '3':
        select_vuz()
        return True
    elif user_answer == '4':
        choice_sotr_and_stat()
        return True
    elif user_answer == '5':
        return False
    else:
        print('Ввведено неправильное значение, введите новое!')
        return True

def main_func():
      #главная функция с выбором задачи
      print('Добро пожаловать в программу! Выберите один из пунктов')
      work = True
      while work:
          print('Вывод всей базы данных - 1')
          print('Вывод таблицы - 2')
          print('Вывод перечень полных наименований вузов, имеющих выбранный статус и расположенных в выбранном округе - 3')
          print('Вывод статистики по ВУЗам - 4')
          print('Выход из программы - 5')
          user_answer = input('Введите число: ')
          work = choice(user_answer)


