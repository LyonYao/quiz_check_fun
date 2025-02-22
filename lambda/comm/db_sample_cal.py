import os
from db_connect import DatabaseConnection 
# 设置环境变量
# os.environ['DB_NAME'] = 'your_database'
# os.environ['DB_USER'] = 'your_username'
# os.environ['DB_PASSWORD'] = 'your_password'
# os.environ['DB_HOST'] = 'localhost'
# os.environ['DB_PORT'] = '5432'

# 创建数据库连接
print(os.getenv('DB_HOST'))
db = DatabaseConnection()
db.connect()
# 调用 execute_update 方法
# update_query = "UPDATE your_table SET column_name = %s WHERE id = %s"
# update_params = ('new_value', 1)
# db.execute_update(update_query, update_params)

# # 调用 execute_insert 方法
# insert_query = "INSERT INTO your_table (column1, column2) VALUES (%s, %s)"
# insert_params = ('value1', 'value2')
# db.execute_insert(insert_query, insert_params)

# # 调用 execute_delete 方法
# delete_query = "DELETE FROM your_table WHERE id = %s"
# delete_params = (1,)
# db.execute_delete(delete_query, delete_params)

# 调用 execute_paged_query 方法
paged_query = "SELECT * FROM quiz.activity_summary"
page = 1
page_size = 10
paged_results = db.execute_paged_query(paged_query, page, page_size)
for row in paged_results:
    print(row)

# 关闭数据库连接
db.close()