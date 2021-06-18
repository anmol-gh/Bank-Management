#imports

import mysql.connector as sql

#Connection to mysql

def connect():
  
#Checking if the database exists or not.
  
  try:
    mycon = sql.connect(host = "localhost",user="root",passwd="123456",database="sys")
    x=mycon.cursor()
    x.execute('select * from bank_details;')
    if x.fetchall()==[]:
      x.execute("INSERT INTO bank_details (First_Name,Last_Name,Account_Number,pass,Age,Balance) "
  "VALUES (%s, %s, %s, %s,%s,%s)",('entry_0','entry_0',0,0,0,0))
    return x,mycon
  
#Creating the database if it doesn't exists.
  
  except:
    mycon = sql.connect(host = "localhost",user="root",passwd="123456",database="sys")
    x=mycon.cursor()
    x.execute('create table bank_details(First_Name char(30),Last_Name char(30),Account_Number int ,pass int,Age int,Balance int,Primary Key(Account_Number));')
    x.execute('select * from bank_details;')
    if x.fetchall()==[]:
      x.execute("INSERT INTO bank_details (First_Name,Last_Name,Account_Number,pass,Age,Balance) "
  "VALUES (%s, %s, %s, %s,%s,%s)",('entry_0','entry_0',0,0,0,0))
    return x,mycon
  
#Greeting window

def welcome():
  print('~~~~~~~~~~~~~Welcome to Pinewood Bank~~~~~~~~~~~~~')
  print ('PRESS 1 TO MAKE A NEW ACCOUNT')
  print('PRESS 2 TO LOG IN TO EXISTING ACCOUNT')
  print('PRESS ANY OTHER KEY TO QUIT')
  choice = input('ENTER YOUR CHOICE!')
  if choice =='1':
    new_account()
  elif choice=='2':
    log_in()

#Creating a new account

def new_account():
  cursor,mycon=connect()
  print('~~~~~~~~~~~ENTER YOUR DETAILS~~~~~~~~~~~')
  fname=input('ENTER YOUR FIRST NAME').title()
  lname=input('ENTER YOUR LAST NAME').title()
  age=int(input('ENTER YOUR AGE'))
  password=ord(fname[0])*age+age+age*55+len(lname)+ord(lname[-1])*23 
  cursor.execute('select * from bank_details')
  account_number=cursor.fetchall()[-1][2]
  b=("INSERT INTO bank_details (First_Name,Last_Name,Account_Number,pass,Age,Balance) "
  "VALUES (%s, %s, %s, %s,%s,%s)")
  cursor.execute(b,(fname,lname,account_number+1,password,age,0))
  mycon.commit()
  print('ACCOUNT CREATED SUCCESFULLY')
  print(f'YOUR ACCOUNT NUMBER IS {account_number+1}')
  print(f'YOUR ACCOUNT PASSWORD IS {password}')
  print('~~~~~~~~~~~YOU ARE BEING REDIRECTED TO MAIN PAGE~~~~~~~~~~~\n')
  welcome()
  
#Log in into an existing account

def log_in():
  cursor,mycon=connect()
  account_number_input=int(input('Enter your Account Number'))
  password_number_input=int(input('Enter your password'))
  get_row='select * from bank_details where account_number=%s'
  cursor.execute(get_row,(account_number_input,))
  a=cursor.fetchall()
  if a==[]:
    print('It seems like you entered invalid credentials')
    print('~~~~~~~~~~~YOU ARE BEING REDIRECTED TO MAIN PAGE~~~~~~~~~~~')
    welcome()
  for i in a:
    if i[3]==password_number_input:
      money(i)
      print('~~~~~~~~~~~YOU ARE BEING REDIRECTED TO MAIN PAGE~~~~~~~~~~~')
      welcome()
    else:
      print('It seems like you entered invalid credentials')
      print('~~~~~~~~~~~YOU ARE BEING REDIRECTED TO MAIN PAGE~~~~~~~~~~~')
      welcome()

#Money debit,credit,balance check

def money(i):
  cursor,mycon=connect()
  print('Welcome',i[0].title(),i[1].title()+', you have successfully logged in')
  print('PRESS 1 TO DEPOSIT MONEY')
  print('PRESS 2 TO WITHDRAW MONEY')
  print('PRESS 3 TO CHECK CURRENT BALANCE')
  money=int(input('Enter your choice'))
  if money==1:
    money_deposit=int(input('How much money you want to deposit? '))+i[-1]
    if money_deposit-i[-1]>0:
      updation='update bank_details set balance=%s where account_number=%s'
      cursor.execute(updation,(money_deposit,i[2]))
      mycon.commit()
      print(money_deposit-i[-1],'credited in your account')
      print('Your current Balance is',money_deposit)
    else:
      print('INVALID AMOUNT GIVEN, PLEASE VERIFY YOUR AMOUNT AGAIN')
  elif money==2:
    money_withdraw=i[-1]-int(input('How much money you want to withdraw? '))
    if money_withdraw<0:
      print('You cannot debit',abs(money_withdraw-i[-1]),'as you only have',i[-1],'money in your account')
    else:
      updation='update bank_details set balance=%s where account_number=%s'
      cursor.execute(updation,(money_withdraw,i[2]))
      mycon.commit()
      print(abs(money_withdraw-i[-1]),'debited from your account')
      print('Your current Balance is',money_withdraw)
  elif money==3:
    print('Your current Balance is',i[-1])
welcome()
