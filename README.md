# splunk-newrelic
Splunk Add-on &amp; App for New Relic
 

## What's Needed?
- Downloads
    - Splunk Add-on for New Relic
    - Splunk App for New Relic


- New Relic Information
    - New Relic Account Number
    - New Relic APM API Key
    - (Optional) New Relic Insights API Key

**Note:** Your New Relic **APM API Key** can be found in your New Relic account here:  
   https://rpm.newrelic.com/accounts/account_number/integrations?page=api_keys


## Installation
The installation consists of installing both the *Splunk Add-on for New Relic* and the *Splunk App for New Relic*.   The Add-on is responsible for executing the rest calls and collecting the data from New Relic.  The App provides the dashboards and saved searches.  To install, navigate to Apps --> Manage Apps and select the “Install app from File” button.  Specify the location of the file you downloaded and install.   

## Configuration
The Splunk Add-on for New Relic contains three separate input types for New Relic data:
- Account Summary
- Single API Call
- Insights Query

In most cases you will only need to use the New Relic Account Summary input.  For each New Relic account that you have, you will enter your New Relic Account Number and API Key and the Input will gather data for your applications, key transaction, mobile applications, alert policy violations.  


## Start Searching
Once the Splunk Add-on for New Relic is installed and configured you can execute searches using: 
```
sourcetype="newrelic_account"
```

----  

# Additional OPTIONAL Configurations
----
# Additional Inputs

### Single New Relic API Call
In some cases you may not want all of the Account Summary data for a given account.  In these cases, or in cases where you may need to execute a different New Relic API call you can use the New Relic Single API Call input type. Use the New Relic API Explorer (https://rpm.newrelic.com/api/explore ) to identify the URL and any associated parameters required for your API call.  Once you have identified the URL and parameters you’ll need to enter those for your new input.  

- Click the **Configure New Input** button and select **New Relic Single API Call**
- Enter your API call parameters and save

Now start searching using 
```
sourcetype="new_relic_single_api_call”
```

### New Relic Insights
New Relic Insights has a separate REST API and requires a separate Insights 'API Key'.  You can find and create Insights QUERY API Keys here:
    https://insights.newrelic.com/accounts/<account_number>manage/api_keys

Once you have identified a New Relic Insights query that you would like run, you’ll need to copy that query and paste it into a new input.  Add a separate Input for each NRQL query you would like to execute.

- Click the **Configure New Input** button and select **New Relic Insights Query**
- Enter the API call parameters and save
    - Name your Query
    - Enter your New Relic Insights Query API Key
    - Enter your New Relic Account Number
    - Enter the NRQL query you would to execute

Now start searching using
```
sourcetype="newrelic_insights"  
```  

-----   

# Sending New Relic Alerts to Splunk 
If you would like to go a step further and have New Relic send Splunk Notifications when Alerts are triggered, you will need to setup 2 components; a Splunk HTTP Event Collector (HEC) Token and a Webhook in New Relic.  

- In Splunk, navigate to Settings, HTTP Event Collector and create a "New Token".  Be sure to set the source value to newrelic_alert so that the dashboards will show your notifications.  
```
source=newrelic_alert
```


- In New Relic, configure a "Notification Channel" in the Alerts section.  
    - The "Base URL" should be: https://your_Splunk_Server:8088/services/collector/raw?channel=HEC_Token  
    - Create a new "Custom Parameter" Named "Authorization" with a value of "Splunk HEC_Token"  
    - Add this Notification Channel to your existing Alert Policies in New Relic and you're all set!  

Now, when New Relic triggers a policy violation, it will be automatically sent to Splunk.


-----   

# Sending Splunk Alerts to New Relic
If you would like to send Splunk Alerts to New Relic Insights, simply create your Splunk Alert and add an alert action to "Send to Relic".    You'll enter your New Relic Insights account and API Key and Splunk forward the alert into New Relic Insights.
