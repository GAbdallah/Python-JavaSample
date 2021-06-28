import psycopg2
from psycopg2 import extras






class DatabaseLayer(object):




    def __init__(self, connection):
        """ Init  """
        self.connection = connection

        
    def set_connection(self, connection):
        """Update the conneciton"""
        self.connection = connection
        



    def get_covering_storee(self, employeeid):
        """ Extarct covering store 

            @:param None
        """
        assert employeeid is not None 
        assert  self.connection is not None 
        
        cov_sp_data_arr = []
        
        cur =  self.connection.cursor()

        assert cur is not None

        query   =  "SELECT U.login as employee_id, SP.sap_number, SP.id " \
                        "FROM res_users U " \
                        "LEFT OUTER JOIN hr_employee E ON E.emp_no = U.login " \
                         "LEFT OUTER JOIN designation_tracker cov_loc ON cov_loc.dealer_id = E.id " \
                        "LEFT OUTER JOIN sap_store SP ON SP.id = cov_loc.store_name " \
                        "WHERE U.active = 'true' AND U.login = %s AND  cov_loc.end_date > now() AND cov_loc.covering_str_check ='1'"

        cur.execute(query, (employeeid,))

        cov_sp_data_arr = cur.fetchone()
        
        return cov_sp_data_arr




        
        

    def get_employee_data(self, employeeid):
        """ Extarct Terminated employee from RDS

            @:param None
        """
        assert employeeid is not None 
        assert  self.connection is not None 
        
        employee_data_array = []
        
        cur =  self.connection.cursor()

        assert cur is not None

        query   =  ""

        cur.execute(query, (employeeid,))

        row = cur.fetchone()
        
        
        cov_store_data = self.get_covering_storee(employeeid)
        
        cov_sap_nbr = ""
        cov_sap_id = ""
        
        if cov_store_data:
            cov_sap_nbr = cov_store_data[1]
            cov_sap_id = cov_store_data[2]

        if row:
            employee_data_array.append(row)

        return employee_data_array
        
        
        
        
    def get_users_password_data(self, employeeid):
        """ Extarct Terminated employee from RDS

            @:param None
        """
        
        assert employeeid is not None 
        assert  self.connection is not None 
        
        
        cur =  self.connection.cursor()
        
        password_data = None

        assert cur is not None

        query   =  "SELECT U.login as employee_id, U.password_crypt " \
                        "FROM res_users U " \
                        "WHERE U.active = 'true' AND U.login = %s"

        cur.execute(query, (employeeid,))

        user_data_arr = cur.fetchone()

        if user_data_arr:
            
            password_data = {  'emp_no': user_data_arr[0], 'password': user_data_arr[1]}

        return password_data



    def insert_login_audit_data(self, value_array):
        """ Extarct Terminated employee from RDS

            @:param None
        """
        assert value_array is not None 
        assert  self.connection is not None 
        
        
        cur =  self.connection.cursor()

        assert cur is not None

        query   = "INSERT INTO wv_tb_login_audit " \
                  "(date, employee_id, ip_address, source, event) VALUES(%s, %s, %s, %s, %s)"

        cur.execute(query, value_array)

        connection.commit()

        cur.close()

        return True