import sqlite3 as sql
from sqlite3 import Error

def sql_connection(database_name="testDB.db"):
    """
    链接数据库：
    database_name : 需要被连接的数据库
    """
    try:
        con=sql.connect(database_name)
        print("Connection is established")
    except Error:
        print(Error)
    return con

def select_table(con,table_name,**kwargs):
    """
    任意表查询：
    table_name : 需要查询的表
    **kwargs : 查询条件（例如：user_name="'xa'"和user_id=1002）     ret=[(1002,...)]
    for user_id,... in ret:
        
    返回 一个用户所有信息
    如果查询错误或者SQL语句错误   返回None
    如果返回[]   则代表查询成功但无结果
    [] 中是一个个元组
    """
    cursor=con.cursor()
    try:
        sql="SELECT * FROM "+table_name+" WHERE "
        flag=0
        values=[]
        for key,value in kwargs.items():
            if flag==1:
                sql=sql+" AND "
            sql=sql+key+"=?"
            values.append(value)
            flag=1
        cursor.execute(sql,tuple(values))
        ret=cursor.fetchall()
        return ret
    except:
        print("Select Failed")
        return None
    
def delete_table_index(con,table_name,**kwargs):
    """
    任意表的元组删除：
    table_name : 需要删除元组所在表
    **kwargs : 删除条件
    """
    cursor=con.cursor()
    try:
        sql="DELETE FROM "+table_name+" WHERE "
        flag=0
        for key,value in kwargs.items():
            if flag==1:
                sql=sql+" AND "
            print(key,value)
            sql=sql+key+"="+str(value)
            flag=1
        cursor.execute(sql)
        con.commit()
        print("Successfully Deleted")
        return True
    except:
        print("Delete Failed")
        con.rollback()
        return False


def delete_table(con,table_name):
    """
    任意表的删除：
    table_name : 需要删除的表
    """
    cursor=con.cursor()
    try:
        sql="DROP TABLE "+table_name
        cursor.execute(sql)
        con.commit()
        print("Table "+table_name+" is deleted")
        return True
    except:
        print("Deleted Failed")
        con.rollback()
        return False
    
def delete_view(con,view_name):
    """
    任意表的删除：
    table_name : 需要删除的表
    """
    cursor=con.cursor()
    try:
        sql="DROP VIEW "+view_name
        cursor.execute(sql)
        con.commit()
        print("View "+view_name+" is deleted")
        return True
    except:
        print("Deleted Failed")
        con.rollback()
        return False



def search_member(con,table_name,group_id):
    """
    查找一个群的所有成员
    """
    member=[]
    try:
        ret=select_table(con,table_name=table_name,group_id=group_id)
        for group_id,member_id in ret:
            member.append(member_id)
        return member
    except:
        print("Search Failed")
        return None
    

def search_firend(con,user_id,table_name="table_relation"):
    """
    查找用户的所有好友ID和关系
    """
    friend=[]
    try:
        ret=select_table(con,table_name,user_id=user_id)
        for user_id,friend_id,relation in ret:
            friend.append((friend_id,relation))
        return friend
    except:
        print("Search Failed")
        return None

def search_all_user(con,table_name="user"):
    """
    查找用户表中的所有群成员
    """
    cursor=con.cursor()
    try:
        sql="SELECT * FROM "+table_name
        cursor.execute(sql)
        ret=cursor.fetchall()
        return ret
    except:
        print("Search Failed")
        return None


def Convert_BLOB(filename):
    """
    将一个文件或图像转化为二进制文件存储
    """
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data



  