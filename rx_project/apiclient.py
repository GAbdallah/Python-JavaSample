# -*- coding: utf-8 -*-
import urllib
import json


# A helper Client for the TrackTraceRX API
class APIClient:

    api_url = ""
    update_api_url = ""
    data = {}





    def __init__(self, api_key, api_secret_key):

           self.data['api_key'] 	= api_key
           self.data['api_secret']      = api_secret_key
       





    
    # Update the status of the Transaction
    # Step  Values
    #
    #o QUEUED : In the Queue to be sent to Bots for Conversion
    #o CONVERSION : Currently converted by bots
    #o SEND: In Hands of Mandelson to be sent
    #o WAIT_ACK: Sent, but waiting the ACK (MDN).
    #o COMPLETED : Received the ACK (MDN).
    #
    # @param int task ID
    # @param String step
    # @param String 'Y' or 'N'
    # @paran String error_msg 
    # @return  Boolean True if the upadate successed and False if there is an error  
    # 
    #
    #
    def update_oubtbound_edi_task(self, task_id, step, success, error_msg= None):
        
        self.data['task_id']    = task_id
        self.data['step']       = step
        self.data['success']    = success
        
        if success == 'N' :
           self.data['error_msg']  = error_msg
        
        #Call the API
        try: 
           urllib.urlopen(self.update_api_url, urllib.urlencode(self.data))
        except Exception as e: 
               return False 
         
        return True 





    # Get available  transaction in the Queue
    # @return JSON transaction data 
    #
    def getNextTransaction(self):
        
        #Connect to the API
        try :
              u = urllib.urlopen(self.api_url, urllib.urlencode(self.data))
        except Exception as e :    
              return {'error':True,'msg':e.message}

        #parse response JSON
        response = u.read()
        
        #Check is there is any error
        if response :
            response = response.decode('utf-8')
            json_data = json.loads(response)
            
            # Check if there is any errors
            if 'error' in json_data:
                return json_data
      
            #Check if there is a task
            if json_data['has_task']:
                return json_data
	    
        return False
