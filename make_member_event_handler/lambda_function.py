import pymysql
import boto3
import os

pymysql.install_as_MySQLdb()

def lambda_handler(event, context):
    conn = pymysql.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        port=3306,
        db=os.environ.get('DB_NAME'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
    )
    event_data = event
    with conn.cursor() as cursor:
        # 새로운 회원 데이터를 추가
        for data in event_data:
            id, dormitory_code, name, phone_number, birthday = data
            # 기존 회원 테이블에서 일치하는 회원 정보가 없는 경우에만 추가
            cursor.execute("SELECT * FROM domtory.member WHERE username = %s", (dormitory_code,))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO domtory.member (username, password, name, phone_number, birthday, status) VALUES (%s, %s, %s, %s, %s, 'ACTIVE')", (dormitory_code, birthday, name, phone_number, birthday))
        conn.commit()
        
    return {
        'statusCode': 200
    }
