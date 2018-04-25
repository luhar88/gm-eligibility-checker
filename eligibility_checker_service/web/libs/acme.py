import json
import os

from web.libs.base_eligibility_check import BaseEligibilityCheck

SCHEMA_FILE = os.path.join('web', 'configs', 'acme_schema.json')
ACME_EMPLOYEE_FILE = os.path.join('web', 'sample_data', 'acme_data.tsv')
PARTNER_METADATA = os.path.join('web', 'sample_data', 'partner_metadata.json')
SUCCESS_MESSAGE = 'Employee %s is eligible'
EMP_ID = 'employee_id'
EMP_NAME = 'employee_name'


class Acme(BaseEligibilityCheck):
    """
    Class for managing eligibility check mechanism for Acme Inc. employees
    """
    def __init__(self, partner_id):
        with open(SCHEMA_FILE, 'r') as f:
            self._schema = json.load(f)
        super(Acme, self).__init__(partner_id, self._schema)
        self._employee_df = self._read_tsv(ACME_EMPLOYEE_FILE)
        self._employee_id_set = set(self._employee_df.employee_id)

    def _check_eligibility(self, data=None):
        emp_id = data.get(EMP_ID)

        if emp_id in self._employee_id_set:
            df = self._employee_df
            emp_name = df.at[df.index[df.employee_id == emp_id].tolist()[0], EMP_NAME]
            self._eligible_message['message'] = SUCCESS_MESSAGE % emp_name
            return self._eligible_message
        else:
            return self._ineligible_message


if __name__ == '__main__':
    e_id1 = {'employee_id': 1}
    e_id2 = {'employee_id': 11}
    e_id3 = {'employee_id': 1111}
    e_id3 = {'employee_ids': 1111}

    av = Acme(partner_id=1)
    # av.config()
    av.check_eligibility(data=e_id1)
    av.check_eligibility(data=e_id2)
    av.check_eligibility(data=e_id3)
