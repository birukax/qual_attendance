from django.test import TestCase
import mysql.connector
import pyodbc
from zk import ZK
from models import Employee, Attendance

connection = "DRIVER={SQL Server};SERVER=172.16.18.23;DATABASE=QualabelsProd_2022_23;"
conn = pyodbc.connect(connection)
if conn:
    print("successful")
cursor = conn.cursor()
employee = cursor.execute(
    "select [No_] as no, [First Name] as fname, [Middle Name] as mname, [Last Name] as lname from [dbo].[QuaLabels Manufacturers$Employee] ORDER BY no"
)
# emp = cursor.fetchall()

# for e in emp:
# print(e)
conn.close()
device_connected = ZK(ip="172.16.19.51", port=4370, timeout=5)
device_connected.connect()

Employee.objects.adelete()
