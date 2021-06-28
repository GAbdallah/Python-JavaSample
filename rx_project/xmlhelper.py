# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from datetime import datetime









# Get the NDC format by spliting the NDC number and
# getting the length of each part example 566-4333-33 give the format 342
#
# @param String the ndc
# @return String the NDC format
#
def get_NDC_Format(ndc):
     ndc_arr = ''
     format = ''
     if '-' in ndc:
      ndc_arr = ndc.split('-')
     
     for i in ndc_arr:
        format += str(len(i))

     return format










#   Wrtie the transaction in the  XML file
#
#  @param JSON data of the transaction
#  @path the path where the XML file will be write
#  @return None
#
def transactionToXML(transactions , path):

    
    root = ET.Element("Shipment")

    ET.SubElement(root, "SenderId").text = transactions['company_id_value']
    ET.SubElement(root, "ReceiverId").text = transactions['tp_id_value']

    #**************************** BSN *************************************
    ET.SubElement(root, "Purpose").text = 'Original'
    #todo
    ET.SubElement(root, "ShipmentID").text ='331'
    ET.SubElement(root, "ShipmentDate").text = transactions['transaction']['ti_shipped_on']
    
    #Get Time
    hour = str(datetime.now().hour)
    minutes = str(datetime.now().minute)
    
    if len(minutes) == 1:
        minutes = '0' + minutes
    
    if len(hour) == 1:
        hour = '0' + hour
    
    ET.SubElement(root, "ShipmentTime").text = hour +':'+ minutes  #To update we just set the current time when the EDI was created
    
    #Hierarchical Structure Code BSN005
    ET.SubElement(root, "HLStructureCode").text = '0001'
    ET.SubElement(root, "TransactionCode").text = 'AS'
    #todo
    ET.SubElement(root, "PackagingCode").text = ''
    ET.SubElement(root, "LadingQty").text = ''
    scac = transactions['transaction']['ti_shipping_carrier']
    if scac and len(scac) < 2   :
        scac = "" 
    ET.SubElement(root, "SCAC").text = scac  
    
    
    #todo same as the shipement ID
    ET.SubElement(root, "BillOfLadingNo").text = ''
    ET.SubElement(root, "ShipDate").text = transactions['transaction']['ti_shipped_on']
    
    ET.SubElement(root, "WeightQualifier").text = ''
    ET.SubElement(root, "Weight").text = ''
    ET.SubElement(root, "WeightUOM").text = ''
    ET.SubElement(root, "CarrierStandardId").text = ''
    ET.SubElement(root, "TransportMethod").text = transactions['transaction']['ti_shipping_method']
    ET.SubElement(root, "ShipmentStatus").text = 'CC'
   
    #BuyingParty
    
    BuyingParty = ET.SubElement(root, "BuyingParty")
    ET.SubElement(BuyingParty, "Name").text = transactions['buyer_address']['name']
    ET.SubElement(BuyingParty, "ID",TYPE="91").text = transactions['buyer_address']['id']
    ET.SubElement(BuyingParty, "City").text = transactions['buyer_address']['city']
    ET.SubElement(BuyingParty, "Address1").text = transactions['buyer_address']['line1']
    ET.SubElement(BuyingParty, "Address2").text = transactions['buyer_address']['line2']
    ET.SubElement(BuyingParty, "PostalCode").text = transactions['buyer_address']['zip']
    ET.SubElement(BuyingParty, "StateCode").text = transactions['buyer_address']['_state_code']
    ET.SubElement(BuyingParty, "CountryCode").text = transactions['buyer_address']['_country_iso2_code']
    
    #ShippingAddress
    ShippingAddress = ET.SubElement(root, "ShippingAddress")
    ET.SubElement(ShippingAddress, "Name").text = transactions['transaction']['ti_address']['name']
    ET.SubElement(ShippingAddress, "ID",TYPE= '91').text = transactions['transaction']['ti_address']['id']
    ET.SubElement(ShippingAddress, "City").text = transactions['transaction']['ti_address']['city']
    ET.SubElement(ShippingAddress, "Address1").text = transactions['transaction']['ti_address']['line1']
    ET.SubElement(ShippingAddress, "Address2").text = transactions['transaction']['ti_address']['line2']
    ET.SubElement(ShippingAddress, "PostalCode").text = transactions['transaction']['ti_address']['zip']
    ET.SubElement(ShippingAddress, "StateCode").text = transactions['transaction']['ti_address']['_state_code']
    ET.SubElement(ShippingAddress, "CountryCode").text = transactions['transaction']['ti_address']['_country_iso2_code']
    
    #Seller
    Seller = ET.SubElement(root, "Seller")
    ET.SubElement(Seller, "Name").text = transactions['transaction']['owner_address']['name']
    ET.SubElement(Seller, "ID",TYPE= '91').text = transactions['transaction']['owner_address']['id']
    ET.SubElement(Seller, "City").text = transactions['transaction']['owner_address']['city']
    ET.SubElement(Seller, "PostalCode").text = transactions['transaction']['owner_address']['zip']
    ET.SubElement(Seller, "Address1").text = transactions['transaction']['owner_address']['line1']
    ET.SubElement(Seller, "Address2").text = transactions['transaction']['owner_address']['line2']
    ET.SubElement(Seller, "StateCode").text = transactions['transaction']['owner_address']['_state_code']
    ET.SubElement(Seller, "CountryCode").text = transactions['transaction']['owner_address']['_country_iso2_code']
    
    #ShipFrom
    shipformAddress  = 'owner_address'
    
    if transactions['transaction']['product_phys_address']:
        shipformAddress = 'product_phys_address'
    
    ShipFrom = ET.SubElement(root, "ShipFrom")
    ET.SubElement(ShipFrom, "Name").text = transactions['transaction'][shipformAddress]['name']
    ET.SubElement(ShipFrom, "ID",TYPE= '91').text = transactions['transaction'][shipformAddress]['id']
    ET.SubElement(ShipFrom, "City").text = transactions['transaction'][shipformAddress]['city']
    ET.SubElement(ShipFrom, "PostalCode").text = transactions['transaction'][shipformAddress]['zip']
    ET.SubElement(ShipFrom, "Address1").text = transactions['transaction'][shipformAddress]['line1']
    ET.SubElement(ShipFrom, "Address2").text = transactions['transaction'][shipformAddress]['line2']
    ET.SubElement(ShipFrom, "StateCode").text = transactions['transaction'][shipformAddress]['_state_code']
    ET.SubElement(ShipFrom, "CountryCode").text = transactions['transaction'][shipformAddress]['_country_iso2_code']
    
    #Transaction Statement
    outbound_ts_1 = transactions['transaction']['outbound_ts_checks_is_auth']
    
    outbound_ts_2 = transactions['transaction']['outbound_ts_checks_received_from_person_auth']
    outbound_ts_3 = transactions['transaction']['outbound_ts_checks_received_ti_and_ts_from_prior_owner']
    
    outbound_ts_4 = transactions['transaction']['outbound_ts_checks_did_not_ship_suspect_or_illegetimate_prd']
    outbound_ts_5 = transactions['transaction']['outbound_ts_checks_had_sys_comply_with_verif_req']
    outbound_ts_6 = transactions['transaction']['outbound_ts_checks_did_not_knowingly_provide_false_trx_info']
    outbound_ts_7 = transactions['transaction']['outbound_ts_checks_did_not_alter_trx_info']
    
    YesNoQuestions  = ET.SubElement(root, "YesNoQuestions")
    if outbound_ts_1 and outbound_ts_2 and outbound_ts_3 and outbound_ts_4 and outbound_ts_5 and outbound_ts_6 and outbound_ts_7:
       YesNoQuestion   = ET.SubElement(YesNoQuestions, "YesNoQuestion")
       ET.SubElement(YesNoQuestion, "IndustryCode").text = 'TS'
       ET.SubElement(YesNoQuestion, "ResponseCode").text = 'Y'
       ET.SubElement(YesNoQuestion, "FreeFormMessageText").text = 'Seller has complied with each applicable subsection of FDCA Sec. 581(27)(A)-(G)'

    #Manufacturer Statement
    outbound_ts_checks_bought_direct_from_manufacturer = transactions['transaction']['outbound_ts_checks_bought_direct_from_manufacturer']
    if outbound_ts_checks_bought_direct_from_manufacturer:
        YesNoQuestion   = ET.SubElement(YesNoQuestions, "YesNoQuestion")
        ET.SubElement(YesNoQuestion, "IndustryCode").text = 'DPS'
        ET.SubElement(YesNoQuestion, "ResponseCode").text = 'Y'
        ET.SubElement(YesNoQuestion, "FreeFormMessageText").text = 'This wholesale distributor, or a member of the affiliate of such wholesale distributor, purchased the product directly from the manufacturer, exclusive distributor of the manufacturer, or repackage that purchased the product directly from the manufacturer'

    #Order
    order = ET.SubElement(root, "Order")
    po_nbr = transactions['transaction']['misc_po_nbr']
    if not po_nbr:
        po_nbr = 'NOPONBR'
    ET.SubElement(order, "PONumber").text = po_nbr
    ET.SubElement(order, "PODate").text = transactions['transaction']['outbound_transaction_date']
    ET.SubElement(order, "SellerInvoiceNumber").text = transactions['transaction']['misc_invoice_id']

    #Item
    item = ET.SubElement(order, "Item")
    lot = transactions['transaction']['lot']
    if '*' in lot:
      lot = lot.replace('*','')
    ET.SubElement(item, "LotNumber").text = lot
    #Extract NDC and formnat
    ndc = transactions['transaction']['ndc']
    ET.SubElement(item, "NDC", FORMAT= get_NDC_Format(ndc) ).text = ndc

    ET.SubElement(item, "VendorCatalogNumber").text = str(transactions['transaction']['item_id'])
    ET.SubElement(item, "UnitsShipped").text = str(transactions['transaction']['serialess_qty'])
    ET.SubElement(item, "UnitsShippedUOM").text = 'EA'
    ET.SubElement(item, "ItemDescType").text = 'F'   #Default value F
    ET.SubElement(item, "ItemDescription").text = transactions['transaction']['product_name']
    ET.SubElement(item, "LotNumberExpiration").text = transactions['transaction']['expiration_date']

    #Manufacturer
    if transactions['transaction']['manufacturer']:
        Manufacturer = ET.SubElement(item, "Manufacturer")
        ET.SubElement(Manufacturer, "Name").text =transactions['transaction']['manufacturer']['name']
        ET.SubElement(Manufacturer, "ID",TYPE= '91').text = transactions['transaction']['manufacturer']['id']
        ET.SubElement(Manufacturer, "City").text =transactions['transaction']['manufacturer']['city']
        ET.SubElement(Manufacturer, "PostalCode").text = transactions['transaction']['manufacturer']['zip']
        ET.SubElement(Manufacturer, "StateCode").text = transactions['transaction']['manufacturer']['_state_code']
        ET.SubElement(Manufacturer, "Address1").text = transactions['transaction']['manufacturer']['line1']
        ET.SubElement(Manufacturer, "Address2").text = transactions['transaction']['manufacturer']['line2']
        ET.SubElement(Manufacturer, "CountryCode").text = transactions['transaction']['manufacturer']['_country_iso2_code']

    if outbound_ts_checks_bought_direct_from_manufacturer:
       YesNoQuestions  = ET.SubElement(item, "YesNoQuestions")
       YesNoQuestion   = ET.SubElement(YesNoQuestions, "YesNoQuestion")
       ET.SubElement(YesNoQuestion, "IndustryCode").text = 'DIR'
       ET.SubElement(YesNoQuestion, "ResponseCode").text = 'Y'
    
    
    tree = ET.ElementTree(root)
    task_id = transactions['task_id']

    # Wrtie the XML file
    filePath = path + '/' + str(task_id) +".xml"
    tree.write(filePath, xml_declaration=True, encoding='utf-8', method="xml")
