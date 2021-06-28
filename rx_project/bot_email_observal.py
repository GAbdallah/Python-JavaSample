# Module partner
"""This class is used to log errors in the console"""

from observer import Observer
import bots.botsglobal as botsglobal
import bots.botslib as botslib




class BotEmail(Observer):
    """Class " to print errors in the console"""
    

    def log_error(self, *args, **kwargs):
        """This function will send email with the error """
        log_data = args[0]
        error_msg = ''
        if 'msg' in log_data:
            error_msg = log_data['msg']
        botsglobal.logger.info(u'The email will be sent : %s',error_msg)
        botslib.sendbotserrorreport('[BOTS EDI Error] ',error_msg)



    def log_info(self, *args, **kwargs):
        """This function will print info message in the BOTS console """
        pass
            



    def send_email(self, msg):
        """This function will send email with the mmessage """
        if msg:
            botslib.sendbotserrorreport('[BOTS EDI INFO] ',msg)




