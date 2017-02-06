
# encoding = utf-8

import os
import sys
import time
import datetime

'''
    IMPORTANT
    Edit only the validate_input and collect_events functions.
    Do not edit any other part in this file.
    This file is generated only once when creating the modular input.
'''
'''
# For advanced users, if you want to create single instance mod input, uncomment this method.
def use_single_instance_mode():
    return True
'''

def validate_input(helper, definition):
    """Implement your own validation logic to validate the input stanza configurations"""
    # This example accesses the modular input variable
    # account_number = definition.parameters.get('account_number', None)
    # api_key = definition.parameters.get('api_key', None)
    pass

def collect_events(helper, ew):
    # Implement your data collection logic here
    import HTMLParser
    import json
    import urllib
    import requests


    #  Process each account input in inputs.conf separately
    #  First we'll get the account ID and api key for each input (stanza in inputs.conf) and then execute the REST API calls
    stanzas = helper.input_stanzas
    for stanza_name in stanzas:
        opt_account = helper.get_arg('account')
        opt_api_key = helper.get_arg('api_key')
        idx = helper.get_output_index()
        st = helper.get_sourcetype()

        # If there are more than 1 input of this type, the arguments will be in a dictionary so grab them out
        if type(opt_api_key) == dict:
            opt_account = opt_account[stanza_name]
            opt_api_key = opt_api_key[stanza_name]
            idx = idx[stanza_name]
            st = st[stanza_name]


        '''
        # Now on to processing this single account
        '''

        #url = "https://api.newrelic.com/v2/applications.json"
        api_base_url = "https://api.newrelic.com/v2/"

        urls = ["applications.json", "key_transactions.json","mobile_applications.json","alerts_violations.json"]

         #headers = {'X-Api-Key':'0d27291dc862905e8e3e8e0f570f0d10b98686e27ffe21d'}
        headers = {'X-Api-Key': '{}'.format(opt_api_key)}
        parameters = "only_open=true"
        account_dict = {'account_id': '{}'.format(opt_account)}

        for i in range(len(urls)):
            url = api_base_url + urls[i]
            if i == 3:
                # /alerts_violations.json --> requires a parameter of 'only_open=true'
                parameters = "only_open=true"
            else:
                parameters = ""

            response = helper.send_http_request(url, "GET", headers=headers,  parameters=parameters, payload=None, cookies=None, verify=None, cert=None, timeout=None, use_proxy=True)

            #r_headers = response.headers
            #r_cookies = response.cookies
            r_json = response.json()
            r_status = response.status_code

            # check the response status, if the status is not sucessful, raise requests.HTTPError
            response.raise_for_status()

            # if all is well, let's add the account ID to the event
            data = json.loads(json.dumps(r_json))
            data.update(account_dict)

            # source=helper.get_input_name()
            src = urls[i]
            event = helper.new_event(source=src, index=idx, sourcetype=st, data=json.dumps(data))
            try:
                ew.write_event(event)
            except Exception as e:
                raise e
       






    """
    # The following examples get the arguments of this input.
    # Note, for single instance mod input, args will be returned as a dict.
    # For multi instance mod input, args will be returned as a single value.
    opt_account = helper.get_arg('account')
    opt_api_key = helper.get_arg('api_key')
    # In single instance mode, to get arguments of a particular input, use
    opt_account = helper.get_arg('account', stanza_name)
    opt_api_key = helper.get_arg('api_key', stanza_name)

    # get input type
    helper.get_input_type()

    # The following examples get input stanzas.
    # get all detailed input stanzas
    helper.get_input_stanza()
    # get specific input stanza with stanza name
    helper.get_input_stanza(stanza_name)
    # get all stanza names
    helper.get_input_stanza_names()

    # The following examples get options from setup page configuration.
    # get the loglevel from the setup page
    loglevel = helper.get_log_level()
    # get proxy setting configuration
    proxy_settings = helper.get_proxy()
    # get user credentials
    account = helper.get_user_credential_by_username("username")
    account = helper.get_user_credential_by_id("account id")
    # get global variable configuration
    global_userdefined_global_var = helper.get_global_setting("userdefined_global_var")

    # The following examples show usage of logging related helper functions.
    # write to the log for this modular input using configured global log level or INFO as default
    helper.log("log message")
    # write to the log using specified log level
    helper.log_debug("log message")
    helper.log_info("log message")
    helper.log_warning("log message")
    helper.log_error("log message")
    helper.log_critical("log message")
    # set the log level for this modular input
    # (log_level can be "debug", "info", "warning", "error" or "critical", case insensitive)
    helper.set_log_level(log_level)

    # The following examples send rest requests to some endpoint.
    response = helper.send_http_request(url, method, parameters=None, payload=None,
                                        headers=None, cookies=None, verify=True, cert=None,
                                        timeout=None, use_proxy=True)
    # get the response headers
    r_headers = response.headers
    # get the response body as text
    r_text = response.text
    # get response body as json. If the body text is not a json string, raise a ValueError
    r_json = response.json()
    # get response cookies
    r_cookies = response.cookies
    # get redirect history
    historical_responses = response.history
    # get response status code
    r_status = response.status_code
    # check the response status, if the status is not sucessful, raise requests.HTTPError
    response.raise_for_status()

    # The following examples show usage of check pointing related helper functions.
    # save checkpoint
    helper.save_check_point(key, state)
    # delete checkpoint
    helper.delete_check_point(key)
    # get checkpoint
    state = helper.get_check_point(key)

    # To create a splunk event
    helper.new_event(data, time=None, host=None, index=None, source=None, sourcetype=None, done=True, unbroken=True)
    """

    '''
    # The following example writes a random number as an event. (Multi Instance Mode)
    # Use this code template by default.
    import random
    data = str(random.randint(0,100))
    event = helper.new_event(source=helper.get_input_type(), index=helper.get_output_index(), sourcetype=helper.get_sourcetype(), data=data)
    ew.write_event(event)
    '''

    '''
    # The following example writes a random number as an event for each input config. (Single Instance Mode)
    # For advanced users, if you want to create single instance mod input, please use this code template.
    # Also, you need to uncomment use_single_instance_mode() above.
    import random
    input_type = helper.get_input_type()
    for stanza_name in helper.get_input_stanza_names():
        data = str(random.randint(0,100))
        event = helper.new_event(source=input_type, index=helper.get_output_index(stanza_name), sourcetype=helper.get_sourcetype(stanza_name), data=data)
        ew.write_event(event)
    '''
