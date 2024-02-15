def create_table_qd(con,table_name="qd"):
    """
    签到表：                                    注：group为关键字，需要输入[group]
    学生学号： student_id
    签到时间： sign_time
    签退时间： sign_out_time
    
    return:
    True : 创建成功    False : 创建失败
    """

    cursor=con.cursor()
    try:
        cursor.execute("CREATE TABLE "+ table_name+" ("
                    "student_id INT PRIMARY KEY,"
                    "sign_time FLOAT,"
                    "sign_out_time FLOAT)")
        con.commit()
        print("table "+table_name+" is created")
        return True
    except Exception as e:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        result = cursor.fetchone()
        if result:
            print("table "+table_name+" is already exists")
        else:
            print("Create Table Failed")
            print(e)
        return False
    
def insert_table_qd(con,table_name,student_id,sign_time,sign_out_time):
    cursor=con.cursor()
    try:
        sql="INSERT INTO "+table_name+" (student_id,sign_time,sign_out_time) VALUES(?,?,?)"
        cursor.execute(sql,(student_id,sign_time,sign_out_time))
        con.commit()
        print("Successfully Insert")
        return True
    except:
        print("Insert Failed")
        con.rollback()
        return False

def update_table_qd(con,table_name,id,index, value):
    """
    用户表更新            输入：
    table_name : 操作的表名
    id : 需要更新信息的用户的ID
    index : 需要更新的选项（例如pwd和email）    注：前面需要加uer_
    value : 更新的值
    """
    cursor=con.cursor()
    try:
        sql="UPDATE "+ table_name +" set "+index+"=? where student_id=?"
        cursor.execute(sql,(value,id))
        con.commit()
        print("Successfully Update")
        return True
    except:
        print("Update Failed")
        con.rollback()
        return False
#实现查询之前签到时间的函数，返回签到时间组成的数组
def query_previous_checkin_times(con,stu_num):
    # 连接到数据库
    cursor = con.cursor()

    # 执行查询
    cursor.execute("SELECT sign_time FROM qd WHERE student_id = ?", (stu_num,))

    # 获取查询结果
    results = cursor.fetchall()

    # 提取签到时间并关闭连接
    checkin_times = [result[0] for result in results]
    con.close()

    return checkin_times  