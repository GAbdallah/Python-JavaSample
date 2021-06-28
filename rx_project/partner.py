# Module partner
"""This class is used to get  partner information like the url, keys etc.."""

import bots.transform as transform
import bots.botslib as botslib


class Partner(object):
    """Class Partner This class manage data relate to a partner"""
    partner_data = {}





    def setup_partner(self, edi_partner_id):
        """ This function search for partner information keys, url.. by  ID's"""
        partner_id = edi_partner_id
        query = "SELECT  partner_id FROM   partner_edi_id WHERE edi_id = '{}' LIMIT 1".format(edi_partner_id)
        
        try :
          for row in botslib.query(query):
            partner_id = row['partner_id']
    
        except Exception as e:
            pass
        
        self.partner_data['name'] = self.get_partner_attr(partner_id, 'name')
        self.partner_data['url'] = self.get_partner_attr(partner_id, 'attr1')
        self.partner_data['key'] = self.get_partner_attr(partner_id, 'attr2')
        self.partner_data['secret_key'] = self.get_partner_attr(partner_id, 'attr3')
        self.partner_data['folder'] = self.get_partner_attr(partner_id, 'attr4')
        self.partner_data['backup'] = self.get_partner_attr(partner_id, 'attr5')





    # @param None
    # @return Dict of data
    def get_partner_infos(self):
        """This function get  information about a partner by looking
            by the partner EDI ID """
        return self.partner_data





    def get_partner_attr(self, edi_partner_id, attr_number):
        """This function is a helper that extract partner attributes """
        return transform.partnerlookup(edi_partner_id, attr_number, safe=True)

