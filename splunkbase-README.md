# Splunk Add-on for New Relic

The Splunk Add-on for New Relic allows a Splunk software administrator to collect data from New Relic APM and New Relic Insights platforms using modular inputs. Data collected from New Relic includes general information about servers, applications, mobile applications, key transactions, policy violations, and New Relic Insights query results. You can then directly analyze the data or use it as a contextual data feed to correlate with other application performance-related data in the Splunk platform.

The Splunk Add-on for New Relic includes field extractions and mappings for the  [Splunk ITSI Module for Application Performance Monitoring](http://docs.splunk.com/Documentation/ITSIAPM/1.0.0/Configure/About).

New Relic APM (application performance monitoring) is New Relic's software analytics product that delivers real-time and trending data about your web application's performance and the level of satisfaction that your end users experience. New Relic Insights is a software analytics resource that gathers and visualizes data from your software to provide information about your business.

You can download the  [Splunk Add-on for New Relic](http://splunkbase.splunk.com/app/3465)  from Splunkbase.

Installation consists of 3 steps:
1. Install the Add-On
2. [Setup Proxy and Logging Configuration](#setup-proxy-and-logging-configuration) (optional)
3. [Create a New Relic Account Input](#create-a-new-relic-account-input)

## Setup Proxy and Logging Configuration
After installing the add-on complete the following steps for setup and configuration of the Add-On and then add Inputs to ingest New Relic data.

### Setup the Splunk Add-on for New Relic

If you are using a proxy or want to change the default logging level (INFO), follow the steps in this section to set up the add-on; otherwise, skip this section.  You can configure the add-on either through the Splunk Web or by making changes directly in the configuration files.

1. On the Splunk Web home screen, click the **Splunk Add-on for New Relic** icon on the Apps sidebar to launch the add-on.
2. In the add-on, click the  **Configuration**  menu.
3.  If you are using a proxy, configure proxy settings under the  **Proxy**  tab. 
	 1. Check  **Enable Proxy**  and fill in the required fields.
	 2. Select the type of proxy to use in the **Proxy Type**  field.
	 3. Provide the proxy server address in the  **Host**  field.
	 4. Provide the proxy server port in the  **Port**  field. For example: 8081.
	 5. Provide a proxy username if you have one in the  **Username**  field.
	 6. If you provided a proxy username, type the proxy password in the  **Password**  field. The Splunk platform encrypts the proxy username and password as soon as you enter these values.
	 7. Check the  **Reverse DNS resolution**  box if you want to perform DNS resolution through your proxy.
	 8. Click  **Save**.
		 If, at any time, you want to disable your proxy but save your configuration, uncheck the  **Enable**  box. The add-on stores your proxy configuration so you can easily enable it again later.  To delete your proxy configuration, delete the values in the fields.

4. Configure the data collection logging level under the  **Logging**  tab.
The data collection logging level defaults to INFO. Optionally, set the logging level under the  **Logging**  tab. You get increasingly more verbose logging in the following order: ERROR, WARN, INFO, DEBUG.


## Create a New Relic Account Input
Configure data inputs to collect data from New Relic APM and New Relic Insights platforms. Data inputs reside on a data collection node, usually a heavy forwarder.  You can configure these inputs either by using [Splunk Web](#configuring-a-new-relic-account-input-in-splunk-web) or by editing  `local/inputs.conf`.

These inputs collect APM information from the New Relic APIs. See the [sourcetypes](#sourcetypes)  for details about what data you can collect.

### Configuring a New Relic Account input in Splunk Web
1.  On your data collection node, access the Splunk Add-on for New Relic.  
2.  Click  **Inputs**.
3.  Click  **Create New Input > New Relic Account Inputs**.
4.  In the Add New Relic Account Inputs window, complete the following fields.

|Setting| Description |
|--:|:--|
| Name | A unique name that identifies the input. |
| Interval | Time interval to collect data, in seconds. Use an interval of less than 300 seconds if you are using this data with the Splunk ITSI Module for Application Performance Monitoring. The default is 60 seconds. | 
| Index | The index in which to store the collected data. | 
| API Key | An API key required to perform user accessible New Relic REST API operations.  If you have not generated a REST API key in New Relic, search for "API keys" in the New Relic documentation. | 
| API URL | One or more API URL endpoints that specify which New Relic APM data to collect. | 
| Account ID | The number that can be found in your New Relic URL. For example, https://rpm.newrelic.com/accounts/<New_Relic_account_number>/applications. | 
    
5.  Click  **Add**.


### Configuring a New Relic Account input in  `inputs.conf`

1.  On your data collection node, create or open your local  `inputs.conf`  file in your add-on directory:
    -   `$SPLUNK_HOME/etc/apps/Splunk_TA_New_Relic/local`  on Unix-based environments
    -   `%SPLUNK_HOME%\etc\apps\Splunk_TA_New_Relic\local`  on Windows environments
2.  Create input stanzas using the following template and example.  
    Template:
     ```
    [new_relic_account_input://<unique_input_name>]
    account = <The number that can be found in your New Relic URL. >
    api_key = <Your API key, required to perform user accessible New Relic REST API operations. If you have not generated a REST API key in New Relic, search for "API keys" in the New Relic documentation.>
    api_url = <API URL endpoints that specify which New Relic APM data to collect, separated by ~. See the example for formatting and possible values.>
    interval = <Time interval in seconds to collect data. Use an interval of less than 300 seconds if you are using this data with the Splunk ITSI Module for Application Performance Monitoring. The default is 60 seconds.>
    index = <The index in which to store the collected data.>
    
    Example:
    [new_relic_account_input://example_input]
    account = 1234567
    api_key = ********
    api_url = applications.json~key_transactions.json~mobile_applications.json~browser_applications.json~servers.json~alerts_events.json~alerts_violations.json
    interval = 60
    index =newrelic
    ```
3.  Save the file.
4.  Restart the data collection node to encrypt your API key.


### Sourcetypes
The Splunk Add-on for New Relic provides the following source types for data collected from New Relic APM and New Relic Insights.

| Input / Source type | Description | ITSI data model |
|--|--|--|
| New Relic API Inputs | 
 | `newrelic:alerts:events`  | General information about Alert events, including ID, event type, description, timestamp, entity data, and incident ID. | None | 
 | `newrelic:alerts:violations` | General information about violations. | None | 
 | `newrelic:applications` | General information about applications monitored by New Relic, including response time, apdex, throughput and settings. | [Application Performance Management](http://docs.splunk.com/Documentation/ITSIAPM/1.0.0/Configure/Datamodel) | 
 | `newrelic:applications:mobile` | General information about mobile applications monitored by New Relic, including active users, interaction time, crash rate, and http error rate. | None
 | `newrelic:servers` | General information about servers monitored by New Relic, including hostname, cpu, and memory stats. | None
 | `newrelic:transactions` | General information about key transactions monitored by New Relic, including response time, apdex, and throughput. | None | 
| New Relic Insights | 
 | `newrelic:insights` | Event data directly collected from New Relic Insights through the Insights Query API. | None | 
|

