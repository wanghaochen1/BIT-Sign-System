def create_table_course(con,table_name="course"):
    """
    课程表：                                    注：group为关键字，需要输入[group]
    课程号： course_id
    任课老师： teacher_id
    已开课次数: kkcs
    
    return:
    True : 创建成功    False : 创建失败
    """

    cursor=con.cursor()
    try:
        cursor.execute("CREATE TABLE "+ table_name+" ("
                    "course_id INT PRIMARY KEY,"
                    "teacher_id INT"
                    "kkcs INT)")
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
    

def insert_table_chat(con,course_id,teacher_id,kkcs,table_name="table_chat"):
    """
    插入课程表：
    course_id : 课程号
    teacher_id : 任课老师编号
    kkcs : 已开课次数
    """
    cursor=con.cursor()
    try:
        sql="INSERT INTO "+table_name+" (course_id,teacher_id,kkcs) VALUES(?,?,?)"
        cursor.execute(sql,(course_id,teacher_id,kkcs))
        con.commit()
        print("Successfully Insert")
        return True
    except:
        print("Insert Error")
        con.rollback()
        return False
    
def update_table_group(con,table_name,course_id, value,index="kkcs"):
    """
    课程表更新            输入：
    table_name : 操作的表名
    course_id : 课程号
    index : 需要更新的选项
    value : 更新的值
    """
    cursor=con.cursor()
    try:
        sql="UPDATE "+ table_name +" set "+index+"=? where course_id=?"
        cursor.execute(sql,(value,course_id))
        con.commit()
        print("Successfully Update")
        return True
    except:
        print("Update Failed")
        con.rollback()
        return False
    

# index=10
# update_table_group(con,"table_course",1,index="kkcs",value=index+1)