# Module commmuincation_script
"""This class send the XML file and communicate  """
import os
import urllib
import urllib2
import json
import tarfile
import shutil
from ConfigParser import SafeConfigParser






class CommuincateScript(object):
    """Class Communicate_script: this class communicate  
        by sending  files that are transalted to a XML files"""
    
    company_api_key = None
    company_secret_key = None
    company_url = None
    backup_folder = None
    folder = None
    filebody = None
    customer_name = None
    
    
    def __init__(self):
        # Load the config and init the paramters
        config_parser = SafeConfigParser()
        config_parser.read('/usr/local/lib/python2.7/dist-packages/bots/config/bots_trx_conf.ini')
        
        self.api_version = config_parser.get('trxapi','api_version')
        self.operation = config_parser.get('trxapi','operation')
        self.document_id = config_parser.get('trxapi','document_id')
        
        self.timeout = config_parser.get('bots','timeout')
        if self.timeout:
            self.timeout = float(self.timeout)
        else:
            self.timeout = 0
        self.qurarantine_dir = config_parser.get('bots','qurarantine_dir')
        self.observers = []



    def setup_connection(self, customer_data):
        """This function setup paramaters to establish a connection 
            to  TRX"""
        self.company_api_key = customer_data['key']
        self.company_secret_key = customer_data['secret_key']
        self.company_url = customer_data['url']
        self.backup_folder = customer_data['backup']
        self.folder = customer_data['folder']
        self.customer_name =customer_data['name']


    # @param doc of the document
    # @return Dict of data
    def send_doc(self, doc):
        """This function get information about a partner by looking
            """
       
        self.__read_doc(doc)
        
        assert self.filebody is not None
        
        data = {}
        data['api_version'] = self.api_version
        data['api_key'] = self.company_api_key
        data['api_secret'] = self.company_secret_key
        data['operation'] = self.operation
        data['document-id'] = self.document_id
        data['document-content'] = self.filebody
        
        info_message = ' DOC : '+ doc +' URL : '+ self.company_url
        log_data = {}
        log_data['name'] = self.customer_name
        log_data['url'] =  self.company_url
        log_data['doc'] =  doc

        try:
            
            response = urllib2.urlopen(self.company_url, urllib.urlencode(data), self.timeout)
            
            # parse response JSON
            json_response = response.read()
            json_data = json.loads(json_response)
            server_error = json_data['error']
            
            if  not server_error:
                #self.__compress_doc(doc)
                self.__delete_doc(doc)
                msg = 'The files have been sent to the API with success '+info_message
                log_data['msg'] = msg
                self.__log_info(log_data)
        
            else:
                if 'msg' in json_data:
                    msg = json_data['msg']
                    msg = 'TrackTrace errors '+msg+' '+ info_message
                    
                    # if the error is the type The Transaction with the Shipment ID "XXXX" already exists
                    # we simply delete the file
                    
                    if 'EDI_PARSER_856BOTSPARSER_DOCUMENT-G00121' in msg:
                        
                            log_data['msg'] = "The duplicate file : "+doc+" is deleted"
                            self.__report_error_and_delete_file(log_data, doc)
                    else:
                            log_data['msg'] = msg
                            self.__report_error_and_delete_file(log_data, doc, True)
    
        except ValueError as error:
            
            msg = str(error)  + 'NBR-0001 Json error '+ info_message
            log_data['msg'] = msg
            self.__report_error_and_delete_file(log_data, doc, True)
        
        except IOError as error:
            
            msg = error.message + 'NBR-0002 URLERROR '+ info_message
            log_data['msg'] = msg
            self.__report_error_and_delete_file(log_data, doc, True)
            
        except Exception as error:
            
            msg = error.message + ' NBR-0003 Unexpected Error '+ info_message
            log_data['msg'] = msg
            self.__report_error_and_delete_file(log_data, doc, True)




    def __report_error_and_delete_file(self, log_data, xml_doc, move_file_flag = None):
        """This function is just a helper function that call
             other function to delete generated XML file
             and report errors, Don't repeat YOUSELF!!!"""
        
        self.__log_error(log_data)
        
        # Check if we can move the file to quarantine folder
        
        if move_file_flag:
            self.__move_doc_to_qurarantine(xml_doc)
        
        self.__delete_doc(xml_doc)




    def __compress_doc(self, doc):
        """This function compress the xml doc """
        # Extract file Name form the path
        file_name = os.path.basename(doc)
        #Compress files
        tar = tarfile.open(self.backup_folder +'/'+file_name+'.bz2', "w:bz2")
        tar.add(doc, arcname=file_name)
        tar.close()
    
    
    
    
    
    def __move_doc_to_qurarantine(self, doc):
        """This function move the doc that generate errors to temporary folder """
        # Copy file to the quraantine folder
        shutil.copy(doc, self.qurarantine_dir)





    def register(self, observer):
        """This function register an oberserval """
        if not observer in self.observers:
            self.observers.append(observer)





    def __log_error(self, error):
        """This function call all register observal to manage the error message """
        for observer in self.observers:
            observer.log_error(error)




    def __log_info(self, info_dict):
        """This function call all register observal to manage the info  message """
        for observer in self.observers:
            observer.log_info(info_dict)




    def __read_doc(self, doc):
        """This function get bots information about a partner by looking
            by the partner EDI ID """
        try:
            xml_file = open(doc, 'rb')
            self.filebody = xml_file.read()
            xml_file.close()
        except IOError as error:
            self.__log_error(error.message + ' NBR-0004 Error during readoing the XML file: '+ doc)



    def __delete_doc(self, doc):
        """This function get bots information about a partner by looking
            by the partner EDI ID """
        try:
            os.remove(doc)
        except IOError as error:
            self.__log_error(error.message + ' NBR-0005 Error unable to delete the XML file: '+ doc)



