#pip install pandas
#pip install ipython
import pandas as pd
import sqlite3
pd.set_option('display.expand_frame_repr', False)
from IPython.display import display
def show_data():
  try:
    con=sqlite3.connect('summary.sqlite')
    cur=con.cursor()
    #Отображение текущего содержимого таблицы БД на экране в виде таблицы
    cur.execute('SELECT * FROM disciplines')
    ar1=cur.fetchall()
    #print(ar1)
    cur.close()
    con.close()
    con=sqlite3.connect('summary.sqlite')
    def my_factory(c,r):
    ###Функция для извлечения имен полей
      d={}
      for i,name in enumerate(c.description):
        d[name[0]]=r[i]
        d[i]=r[i]
      return(d)
    con.row_factory=my_factory
    cur=con.cursor()
    cur.execute('SELECT * FROM disciplines')
    ar=cur.fetchone()
    cur.close()
    con.close()
    fld_names=list(ar.keys())[::2]
    df = pd.DataFrame(columns = fld_names)
    for i in range(len(ar1)):
      df.loc[i] = ar1[i]
    df.set_index('code', inplace = True)
    display(df)
    return df
  except AttributeError:
    print("Oops!  That was empty table.  Try again...")

def save_data():
  name = input('Введите имя файла: ')
  gh=open(name+'.txt','w')
  con=sqlite3.connect('summary.sqlite')
  cur=con.cursor()
  #Отображение текущего содержимого таблицы БД на экране в виде таблицы
  cur.execute('SELECT * FROM disciplines')
  ar1=cur.fetchall()
  def my_factory(c,r):
  ###Функция для извлечения имен полей
    d={}
    for i,name in enumerate(c.description):
      d[name[0]]=r[i]
      d[i]=r[i]
    return(d)
  con.row_factory=my_factory
  cur=con.cursor()
  cur.execute('SELECT * FROM disciplines')
  ar=cur.fetchone()
  cur.close()
  con.close()
  fld_names=list(ar.keys())[::2]
  for r in fld_names:
    gh.write(r + ' ')
  for i in ar1:
    gh.write('\n')
    for j in i:
      gh.write(str(j) + ' ')
  gh.close()

def find_data():
  con=sqlite3.connect('summary.sqlite')
  cur=con.cursor()
  ar = input('Введите условие: ')
  sql="""\
  SELECT * FROM disciplines WHERE
  """ + ar
  cur.execute(sql)
  ar1=cur.fetchall()
  #print(ar1)
  con.commit()
  cur.close()
  con.close()
  con=sqlite3.connect('summary.sqlite')
  def my_factory(c,r):
  ###Функция для извлечения имен полей
    d={}
    for i,name in enumerate(c.description):
      d[name[0]]=r[i]
      d[i]=r[i]
    return(d)
  con.row_factory=my_factory
  cur=con.cursor()
  cur.execute('SELECT * FROM disciplines')
  ar=cur.fetchone()
  cur.close()
  con.close()
  fld_names=list(ar.keys())[::2]
  df = pd.DataFrame(columns = fld_names)
  for i in range(len(ar1)):
    df.loc[i] = ar1[i]
  df.set_index('code', inplace = True)
  display(df)

def action_with_data():
  while True:
    inp = input('Замена/Удаление ').lower()
    if inp == 'замена':
      con=sqlite3.connect('summary.sqlite')
      cur=con.cursor()
      ar = input('Введите имя поля: ')
      num = input('Введите новое значение: ')
      sql="""\
      UPDATE disciplines SET
      """ + ar + '=' + num
      cur.execute(sql)
      ar1=cur.fetchall()
      #print(ar1)
      con.commit()
      cur.close()
      con.close()
      break
      break
    elif inp == 'удаление':
      con=sqlite3.connect('summary.sqlite')
      cur=con.cursor()
      ar = input('Введите условие: ')
      sql="""\
      DELETE FROM disciplines WHERE
      """ + ar
      cur.execute(sql)
      #ar1=cur.fetchall()
      #print(ar1)
      con.commit()
      cur.close()
      con.close()
      break
    else:
      print("Неправильный ввод")

def add_data():
  print('Введите данные: ')
  arr = []
  arr.append(input('Код дисциплины по учебному плану - '))
  arr.append(input('Название дисциплины - '))
  arr.append(int(input('Номер семестра с аттестацией по дисциплине - ')))
  arr.append(input('Тип аттестации (экзамен/зачет) - '))
  arr.append(input('Дата аттестации - '))
  arr.append(input('ФИО преподавателя, проводившего аттестацию - '))
  arr.append(input('Должность преподавателя - '))
  arr.append(int(input('Полученная оценка - ')))
  arr.append(input('Дата занесения/обновления записи - '))
  arr = tuple(arr)
  ar = []
  ar.append(arr)
  con=sqlite3.connect('summary.sqlite')
  cur=con.cursor()
  sql="""\
  INSERT INTO disciplines (code, discipline, term, type_certification , 
data_certification, fio_p , post , mark , data_mark ) VALUES (?,?,?,?,?,?,?,?,?)
  """
  cur.executemany(sql,ar)
  con.commit()
  cur.close()
  con.close()

def user_choice():
  print('Отображение текущего содержимого таблицы БД на экране в виде таблицы - 1')
  print('Сохранение текущего содержимого таблицы БД в текстовый файл с задаваемым именем - 2')
  print('Выбор имени одного из полей БД и задание условия по значениям этого поля. Отображение строк, удовлетворяющих заданному условию - 3')
  print('Операции с подмножеством строк: удаление из БД, замена значений во всех строках в указанном поле на заданное значение - 4')
  print('Добавление новой строки с заданными значениями полей в таблицу БД - 5')
  print('Завершение работы с программой - 6')
  while True:
    print('Выберите действие(введите cсоответствующее число):')
    command = input()
    if command == '1':
      show_data()
    elif command == '2':
      save_data()
    elif command == '3':
      find_data()
    elif command == '4':
      action_with_data()
    elif command == '5':
      add_data()
    elif command == '6':
      break

while True:
    print('Начать работу? (да/нет)')
    user_input = input().lower()
    if user_input == 'да':
      user_choice()
      break
    elif user_input == 'нет':
      break
    else:
      print('Введите корректное значение!')
