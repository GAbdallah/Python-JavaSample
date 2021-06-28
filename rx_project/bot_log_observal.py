# Module partner
"""This class is used to log errors in the console"""

from observer import Observer
import bots.botsglobal as botsglobal
import bots.botslib as botslib
from datetime import datetime



class BotLog(Observer):
    """Class  to print errors in the console"""
    

    def log_error(self, *args, **kwargs):
        """This function will print error in the  console """
        log_data = args[0]
        error_msg = ''
        if 'msg' in log_data:
            error_msg = log_data['msg']
        
        log_data['status'] = 'ERROR'
        botsglobal.logger.error(error_msg)
        self.__save_log(log_data)



    def log_info(self, *args, **kwargs):
        """This function will print info message in the  console """
        log_data = args[0]
        info_msg = ''
        if 'msg' in log_data:
            info_msg = log_data['msg']
        
        log_data['status'] = 'SENT'
        
        botsglobal.logger.info(info_msg)
        
        self.__save_log(log_data)
            
            
            
    def __save_log(self, data):
        """This function save  the  message into database """
        created_on = datetime.now()
        created_on = created_on.strftime('%Y-%m-%d %H:%M:%S')
        botslib.changeq(u'''INSERT INTO trx_log (created_on,error_msg,customer,url,xml_name,status)
            VALUES  (%(created_on)s,%(error_msg)s,%(customer)s,%(url)s,%(xml_name)s,%(status)s)''',
                        {'created_on':created_on, 'error_msg':data['msg'], 'customer':data['name'],
                        'url':data['url'], 'xml_name':data['doc'], 'status':data['status']})


