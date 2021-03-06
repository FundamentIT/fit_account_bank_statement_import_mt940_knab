# -*- coding: utf-8 -*-
"""Implement BankStatementParser for MT940 IBAN ING files."""
##############################################################################
#
#    Copyright (C) 2014-2015 Therp BV <http://therp.nl>.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import re
from odoo.addons.account_bank_statement_import_mt940_base.mt940 import (MT940, str2amount, get_subfields, handle_common_subfields)


class MT940Parser(MT940):
    """Parser for ing MT940 bank statement import files."""

    tag_61_regex = re.compile(
        r'^(?P<date>\d{6})(?P<line_date>\d{0,4})'
        r'(?P<sign>[CD])(?P<amount>\d+?),(?P<amount_decimals>.*?)N(?P<type>.{3})'
        r'(?P<reference>.*)\/\/(?P<bank_reference>.*)'
    )

    def __init__(self):
        """Initialize parser - override at least header_regex."""
        super(MT940Parser, self).__init__()
        self.mt940_type = 'KNAB'
        self.header_lines = 0  # Number of lines to skip


    def handle_tag_61(self, data):
        """get transaction values"""
        super(MT940Parser, self).handle_tag_61(data)
        re_61 = self.tag_61_regex.match(data)
        if not re_61:
            raise ValueError("Cannot parse %s" % data)
        parsed_data = re_61.groupdict()
        if parsed_data['amount_decimals'] == '':
            parsed_data['amount_decimals'] = '00'
        self.current_transaction['amount'] = (
            str2amount(parsed_data['sign'], parsed_data['amount'] + ',' + parsed_data['amount_decimals']))
        self.current_transaction['ref'] = parsed_data['reference']
        self.current_transaction['unique_import_id'] = parsed_data['bank_reference']

    def handle_tag_86(self, data):
        """Parse 86 tag containing reference data."""
        if not self.current_transaction:
            return
        codewords = ['RTRN', 'BENM', 'ORDP', 'CSID', 'BUSP', 'MARF', 'EREF',
                     'PREF', 'REMI', 'ID', 'PURP', 'ULTB', 'ULTD',
                     'CREF', 'IREF', 'CNTP', 'ULTC', 'EXCH', 'CHGS', 'TRTP', 'IBAN', 'BIC', 'NAME']
        subfields = get_subfields(data, codewords)
        transaction = self.current_transaction
        # If we have no subfields, set message to whole of data passed:
        if not subfields:
            transaction['name'] = data
        else:
            handle_common_subfields(transaction, subfields)
            if not transaction.get('name') or transaction['name'] == '':
                #transaction['name'] = subfields['TRTP'] + ' - ' + subfields['IBAN'] + ' (' + subfields['BIC'] + ') '+subfields['NAME']
                transaction['name'] = '{} - {} {} - {}'.format(subfields['TRTP'][0], subfields['IBAN'][0], subfields['BIC'][0],
                                                               subfields['NAME'][0])
        # Prevent handling tag 86 later for non transaction details:
        self.current_transaction = None