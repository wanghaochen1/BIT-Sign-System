def create_table_teacher(con, table_name="teacher"):
    """
    学生表：
    teacher_id : 教师编号
    teacher_name : 教师姓名
    student_pwd : 教师密码
    """
    cursor=con.cursor()
    try:
        cursor.execute("CREATE TABLE "+ table_name+" ("
                  "teacher_id INT PRIMARY KEY,"
                  "teacher_name text,"
                  "teacher_pwd text)")
        con.commit()
        print("table is created")
        return True
    except:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        result = cursor.fetchone()
        if result:
            print("table "+table_name+" is already exists")
        else:
            print("Create Table Failed")
        return False


def insert_table_teacher(con,table_name,teacher_id ,teacher_name,teacher_pwd):
    """
    用户表添加：
    teacher_id : 用户ID
    teacher_name : 用户名
    teacher_pwd : 用户密码
    """
    cursor=con.cursor()
    try:
        sql="INSERT INTO "+table_name+" (teacher_id,teacher_name,teacher_pwd) VALUES(?,?,?)"
        cursor.execute(sql,(teacher_id,teacher_name,teacher_pwd))
        con.commit()
        print("Successfully Insert")
        return True
    except: 
        print("Insert Error")
        con.rollback()
        return False

def update_table_teacher(con,table_name,id,index, value):
    """
    用户表更新            输入：
    table_name : 操作的表名
    id : 需要更新信息的用户的ID
    index : 需要更新的选项（例如pwd和email）    注：前面需要加uer_
    value : 更新的值
    """
    cursor=con.cursor()
    try:
        sql="UPDATE "+ table_name +" set "+index+"=? where user_id=?"
        cursor.execute(sql,(value,id))
        con.commit()
        print("Successfully Update")
        return True
    except:
        print("Update Failed")
        con.rollback()
        return False

