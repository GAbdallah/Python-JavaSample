from database import DatabaseLayer
from passlib.hash import pbkdf2_sha512
from datetime import datetime
from psycopg2 import pool
import psycopg2










rds_database = ''
rds_user = ''
rds_password = ''
rds_host = ''
rds_port = ''

ip = ''

source = 'phone'





postgreSQL_pool = psycopg2.pool.ThreadedConnectionPool(5, 20,
                                              user = "postgres",
                                              password = rds_password,
                                              host = rds_host,
                                              port = rds_port,
                                              database = rds_database)
                                              
                                              
                                              
                                              

ps_connection  = postgreSQL_pool.getconn()

databaseLayer = DatabaseLayer(ps_connection)
                                              

    


def check_if_connection_isdead(ps_connection):
    """ Check if connection is dead or closed 
    """
    assert postgreSQL_pool is not None
    if not ps_connection or ps_connection.closed !=0:
        ps_connection  = postgreSQL_pool.getconn()
        if databaseLayer:
             databaseLayer.set_connection(ps_connection)
        else:
             databaseLayer = DatabaseLayer(ps_connection)
    
    




def run_job(event):
    
    
    if event['body']['employee_id'] and event['body']['password'] and event['method'] == 'POST' and event['body']:
        
        # Check the connection to DB
        
        check_if_connection_isdead(ps_connection)
        
        # Here we get's the employee data and encrypted password from the users table
        
        employee_id = event['body']['employee_id']
        
        entered_password = event['body']['password']
    
        encrypted_data = databaseLayer.get_users_password_data(employee_id)
        
        # Checks data we get the data or not
    
        if encrypted_data:
    
            original_password = encrypted_data['password']
    
            emp_id = encrypted_data['emp_no']
    
            verification = pbkdf2_sha512.verify(entered_password, original_password)
    
            if verification:
    
                event = 'successful_login'
                
                employee_data = databaseLayer.get_employee_data(employee_id)
                
                response = {
                    
                 'statusCode': 200,
                 
                 'body': employee_data
                    
                }
            
                return response
    
       
            
    
        
    response = {
            
            'statusCode': 400,
            
            'body': 'Not a valid data or request'
            
            
        }
        
    return response


def lambda_handler(event, context):
    
    response = run_job(event)
   
    # TODO implement
    return response
    
