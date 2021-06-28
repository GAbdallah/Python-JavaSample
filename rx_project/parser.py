# Module parser
"""This class is used to parse the Xml generated form  and extract data form this doc"""
from xml.etree.ElementTree import parse





class Parser(object):
    """Class parse the XML data"""
    

    def setup_parser(self, doc):
        self.xml_doc = parse(doc)
        self.xml_doc_root = self.xml_doc.getroot()
        self.list_validate_funct = []



    # @param func function
    #
    # @return None
    #
    def add_validator(self, func):
        """This method add validation function to the list"""
        # Check if the func is a real function
        if callable(func) and func not in self.list_validate_funct:
                self.list_validate_funct.append(func)





    #
    # @return  boolean
    #
    # @exception raise Exception when the node ReceiverID is not found
    #
    def is_a_duplicate_asn(self):
        """This method return the partner id from the XML DOC"""
        asn_status = self.xml_doc_root.find('Purpose')
        try:
            if asn_status.text != "Original":
                return True
        except:
            raise Exception('Invalid document! The Purpose node is not available in the document')
        
        return False






    #
    # @return String the partner Shipemnet ID
    # @exception raise Exception when the node ReceiverID is not found
    #
    def get_partner_shipement_id(self):
        """This method return the partner id from the XML DOC"""
        shipement_id = self.xml_doc_root.find('ShippingAddress/ID')
        try:
            return shipement_id.text
        except:
            raise Exception('Invalid document! The ShippingAddress node is not available in the document')





    # @param None
    # @return Integer the partner EDI ID
    # @exception raise Exception when the node ReceiverID is not found
    #
    def get_partner_id(self):
        """This method return the partner id from the XML DOC"""
        receiver_node = self.xml_doc_root.find('ReceiverId')
        try:
            return receiver_node.text
        except:
            raise Exception('Invalid document! The ReceiverID node is not available in the document')


    # @param None
    # @return Boolean True or False
    def is_valide_doc(self):
        """This method check if the doc is valide or not, the process of validation is 
            based of some """
        # Execute all function in the list to validate the doc
        for func in self.list_validate_funct:
            result = func()
            if not result:
                return False

        return True

