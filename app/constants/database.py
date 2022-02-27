from dotenv import dotenv_values

config = dotenv_values('.env')

print(config)
mysqlDomain = config['MYSQL_HOST'] or 'localhost'
mysqlPort = int(config['MYSQL_PORT']) or 3306
mysqlUser = config['MYSQL_USER'] or 'root'
mysqlPassword = config['MYSQL_PASSWORD'] or 'password'
mysqlDatabase = config['MYSQL_DATABASE'] or 'database'
