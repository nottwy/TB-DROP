import pymysql


conn = pymysql.connect(host="localhost",
                       user="root",
                       password="123456",
                       database='tb_drp',
                       charset="utf8")

##upload
def input2mysql(sample_id, left_file_name, right_file_name,status):  # password 一定要转变为字符串   用户注册模块
    cursor = conn.cursor()
    sql = " insert into sample_info(sample_id,left_file_name,right_file_name, time,status) values ('" + sample_id + \
          "','" + left_file_name + "','" + right_file_name + "',CURRENT_TIMESTAMP,'" + status + "')"
    try:
        cursor.execute(sql)
    except:
        conn.ping()
        cursor = conn.cursor()
        cursor.execute(sql)
    conn.commit()


def isrepeatSampleid(sample_id):
    cursor = conn.cursor()
    sql = "select sample_id from sample_info where sample_id='" + sample_id+"'"
    try:
        cursor.execute(sql)
    except:
        conn.ping()
        cursor = conn.cursor()
        cursor.execute(sql)
    sample_id = cursor.fetchall()
    if sample_id == ():
        conn.commit()
        return False
    else:
        conn.commit()
        return True


##upload_data_list

def table2output():
    cursor = conn.cursor()
    sql = "select * from sample_info"
    try:
        cursor.execute(sql)
    except:
        conn.ping()
        cursor = conn.cursor()
        cursor.execute(sql)
    data = cursor.fetchall()
    conn.commit()
    return data

##analysis

def isrepeatID(id):
    cursor = conn.cursor()
    sql = "select status from sample_info where id=" + str(id)
    try:
        cursor.execute(sql)
    except:
        conn.ping()
        cursor = conn.cursor()
        cursor.execute(sql)
    status = cursor.fetchall()
    if status == 'submitted':
        conn.commit()
        return False
    elif status =='finished' or status =='running':
        conn.commit()
        return True
    


def select_info(id):
    cursor = conn.cursor()
    sql = "select sample_id from sample_info where id=" + str(id)
    try:
        cursor.execute(sql)
    except:
        conn.ping()
        cursor = conn.cursor()
        cursor.execute(sql)
    sample_id = cursor.fetchall()
    if sample_id == ():
        return sample_id
    else:
        sample_id = sample_id[0][0]
        sql = "select left_file_name,right_file_name from sample_info where sample_id='" + sample_id + "'"

        try:
            cursor.execute(sql)
        except:
            conn.ping()
            cursor = conn.cursor()
            cursor.execute(sql)
        filename = cursor.fetchall()
        return sample_id, filename


def updatetable(id, status):
    cursor = conn.cursor()
    sql = "update  sample_info set status='"+status+"' where id=" + str(id)
    try:
        cursor.execute(sql)
    except:
        conn.ping()
        cursor = conn.cursor()
        cursor.execute(sql)
    conn.commit()


def inputmysql(id, drug, phenotype):  #模拟运算完成后 将结果输入mysql
    cursor = conn.cursor()
    sql = " insert into result_info(id,drug,phenotype) values (" + str(id) + \
          ",'" + drug + "','" + phenotype + "')"
    try:
        cursor.execute(sql)
    except:
        conn.ping()
        cursor = conn.cursor()
        cursor.execute(sql)
    conn.commit()


def existRunning():
    cursor = conn.cursor()
    sql = "select id,sample_id from sample_info where status= 'running'"
    try:
        cursor.execute(sql)
    except:
        conn.ping()
        cursor = conn.cursor()
        cursor.execute(sql)
    result = cursor.fetchall()
    if result == ():
        conn.commit()
        return False
    else:
        conn.commit()
        return result


## result
def ID2SampleID(id):
    cursor = conn.cursor()
    sql = "select sample_id from sample_info where id=" + str(id)
    try:
        cursor.execute(sql)
    except:
        conn.ping()
        cursor = conn.cursor()
        cursor.execute(sql)
    sample_id = cursor.fetchall()
    conn.commit()
    return sample_id[0][0]


def table2outputByID(id):
    cursor = conn.cursor()
    sql = "select * from result_info where id=" + str(id)
    try:
        cursor.execute(sql)
    except:
        conn.ping()
        cursor = conn.cursor()
        cursor.execute(sql)
    data = cursor.fetchall()
    conn.commit()
    return data


##delete
def delete_sample(id):
    cursor= conn.cursor()
    sql = "delete from sample_info where id = "+str(id)
    try:
        cursor.execute(sql)
    except:
        conn.ping()
        cursor = conn.cursor()
        cursor.execute(sql)
    conn.commit()

