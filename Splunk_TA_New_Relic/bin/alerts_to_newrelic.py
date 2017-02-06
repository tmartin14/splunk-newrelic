
# encoding = utf-8
# Always put this line at the beginning of this file
import splunk_ta_new_relic_declare 

import os
import sys

from alert_actions_base import ModularAlertBase 
import modalert_alerts_to_newrelic_helper

class AlertActionWorkeralerts_to_newrelic(ModularAlertBase):

    def __init__(self, ta_name, alert_name):
        super(AlertActionWorkeralerts_to_newrelic, self).__init__(ta_name, alert_name)

    def validate_params(self):

        if not self.get_param("account"):
            self.log_error('account is a mandatory parameter, but its value is None.')
            return False

        if not self.get_param("apikey"):
            self.log_error('apikey is a mandatory parameter, but its value is None.')
            return False

        if not self.get_param("eventtype"):
            self.log_error('eventtype is a mandatory parameter, but its value is None.')
            return False
        return True

    def process_event(self, *args, **kwargs):
        status = 0
        try:

            if not self.validate_params():
                return 3 
            status = modalert_alerts_to_newrelic_helper.process_event(self, *args, **kwargs)
        except (AttributeError, TypeError) as ae:
            self.log_error("Error: {}. Please double check spelling and also verify that a compatible version of Splunk_SA_CIM is installed.".format(ae.message))
            return 4
        except Exception as e:
            msg = "Unexpected error: {}."
            if e.message:
                self.log_error(msg.format(e.message))
            else:
                import traceback
                self.log_error(msg.format(traceback.format_exc()))
            return 5
        return status

if __name__ == "__main__":
    exitcode = AlertActionWorkeralerts_to_newrelic("Splunk_TA_New_Relic", "alerts_to_newrelic").run(sys.argv)
    sys.exit(exitcode)
