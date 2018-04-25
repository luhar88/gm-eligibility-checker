import jsonschema
import pandas as pd

from web.exceptions import exception as e

ELIGIBLE_MESSAGE = {
    "eligible": True,
}
INELIGIBLE_MESSAGE = {
    "eligible": False,
    "message": "Employee ID does not exist"
}
INVALID_SCHEMA_MESSAGE = 'Invalid schema'


class BaseEligibilityCheck(object):
    """
    Base class for managing eligibility check mechanism
    """
    def __init__(self, partner_id, schema):
        self._schema = schema
        self._eligible_message = ELIGIBLE_MESSAGE
        self._ineligible_message = INELIGIBLE_MESSAGE
        self._partner_id = partner_id

    def config(self):
        return self._schema

    def _validate(self, data):
        """Validate a given schema

        :params args:
            data: Employee data as per given schema
        """
        try:
            jsonschema.validate(data, self._schema)
        except Exception:
            raise e.InvalidSchema

    def _check_eligibility(self, *args, **kwargs):
        raise NotImplementedError

    def check_eligibility(self, *args, **kwargs):
        """
        Validates the data against partner schema and checks if an employee is eligible

        :param args:
            None
        :param kwargs:
            data: Object as per partner schema

            e.g. For the following schema
            {
              "type": "object",
              "properties": {
                "employee_id": {"type": "number"}
              }
            }
            data = {'employee_id': 1}

        :return:
            Returns a tuple with the status, and message
            e.g.
                ('invalid_schema', '')
                ('success', {})
                ('not_found', {})
        """
        try:
            self._validate(kwargs['data'])
            result = ('success', self._check_eligibility(*args, **kwargs))
        except e.InvalidSchema:
            result = ('invalid_schema', INVALID_SCHEMA_MESSAGE)
        except Exception:
            result = ('unknown_error', '')

        return result

    @staticmethod
    def _read_tsv(file_path):
        return pd.read_table(file_path, sep='\t')
