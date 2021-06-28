# import lib

import bots.botsglobal as botsglobal
import bots.botslib as botslib
import os
import glob
from partner import Partner
from parser import Parser
from  bot_log_observal import BotLog
from communication_script import CommuincateScript

def connect(channeldict,*args,**kwargs):
    ''' function does nothing but it is required.'''
    pass


def disconnect(channeldict,*args,**kwargs):
    # Parameters that must be filed for every partner
    
    path =  channeldict['path']+'/'+'*.xml'
    # Get All XML files form the folder into List
    xml_files = glob.glob(path)
    
    # Setup Class's
    parser_ = Parser()
    customer = Partner()
    connection = CommuincateScript()
    logger = BotLog()
    connection.register(logger)
    # Setup
    setup_parser = parser_.setup_parser
    setup_customer = customer.setup_partner
    setup_connection = connection.setup_connection
    # Get partner ID
    for xml in xml_files:
        # Setup the Parser
        setup_parser(xml)
        customer_id = parser_.get_partner_id()
        # Setup the customer
        setup_customer(customer_id)
        data = customer.get_partner_infos()
        
        # Setup  the connection
        setup_connection(data)
        # Send the doc
        connection.send_doc(xml)



