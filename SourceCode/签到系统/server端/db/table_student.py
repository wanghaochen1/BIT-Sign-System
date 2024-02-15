def create_table_student(con, table_name="student"):
    """
    学生表：
    student_id : 学号
    student_name : 学生姓名
    student_pwd : 学生密码
    student_image : 学生人脸二进制文件
    """
    cursor=con.cursor()
    try:
        cursor.execute("CREATE TABLE "+ table_name+" ("
                  "student_id INT PRIMARY KEY,"
                  "student_name text,"
                  "student_pwd text,"
                  "student_image text)")
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


def insert_table_student(con,table_name,student_id ,student_name,student_pwd,student_image):
    """
    用户表添加：
    student_id : 用户ID
    student_name : 用户名
    student_pwd : 用户密码
    student_iamge : 学生人脸图片路径
    """
    cursor=con.cursor()
    try:
        sql="INSERT INTO "+table_name+" (student_id,student_name,student_pwd,student_image) VALUES(?,?,?,?)"
        cursor.execute(sql,(student_id,student_name,student_pwd,student_image))
        con.commit()
        print("Successfully Insert")
        return True
    except: 
        print("Insert Error")
        con.rollback()
        return False

def update_table_student(con,table_name,id,index, value):
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

