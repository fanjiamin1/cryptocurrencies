#pip3 install mysqlclient
import MySQLdb

host = "localhost"
user = "root"
passwd = "root"
dbname = "cryptocurrencies"
port = 49
socket = "/Applications/MAMP/tmp/mysql/mysql.sock"

db = MySQLdb.connect(host, user, passwd, dbname, port, socket)