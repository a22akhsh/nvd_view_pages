CVE-NVD Vulnerabilities Analysis
================================

Project Description
-------------------
This project for analysis of reported vulnerabilities for the software's running over internet or cyber
physical infrastructure. The reported vulnerabilities are based on available open repositories for reported 
critical infrastructure software for example https://nvd.nist.gov/.

Project Work
------------
The project work is conducted for generating report that shows the following analysis points:
1. Total reported vulnerabilities across year.
2. Total reported vulnerabilities for CPS component RTU, MTU, PLC, HMI.
3. Total average cvss score for reported vulnerabilities of CPS components above.
4. Comparison of average CPS score vs the frequency of occurrence for reported vulnerabilities about CPS components.
5. Check manually description of 3 CVE ID for selected year.

All above analysis requirements are handled graphically also using plotly and matplotlib.

'Note: The first time execution is slow because it will try to pull zipped vulnerabilities for all years from open source database.'

Project Architecture
--------
The project is based on MVC (Model, View and Controller) framework.
This nvd_view is view part of the system which interacts with user.
Authenticates and allows the request to be send towards controller and then
the controller based on use case creates response with appropriate
data and status code.
The view is responsible to provide interactiveness to the application with
appropriate security measures.

Request as input
-------
The requests are task based created. Such as:

Task 3.1: The output chart displays total vulnerabilities reported per year. Range must be within 2002-2023.
URL: https://host:port/v1/nvd_view?task=3.1&range=yyyy-yyyy

Task 3.2: The output chart displays total vulnerabilities reported per year for critical infrastructure components
.URL: https://host:port/v1/nvd_view?task=3.2

Task 3.2: The output chart displays cvss score for reported vulnerabilities for critical infrastructure components
.URL: https://host:port/v1/nvd_view?task=3.2.cvss

Task 4.1: The output chart visualize graphically in a chart the number of vulnerability report instances
corresponding to each of these threats. URL: https://host:port/v1/nvd_view?task=4.1

Task 4.2: The output chart visualize graphically correlation of vulnerability report instances
corresponding to each of these threats. URL: https://host:port/v1/nvd_view?task=4.2

Task 4.3: The output chart visualize graphically correlation and frequency of vulnerability report instances
corresponding to each of these threats. URL: https://host:port/v1/nvd_view?task=4.3

Access over web browser
-------
The service will be created after deployment with type NodePort.
Use port-forward command to expose internal port to outside which will enable the access to web browser.
For example:
kubectl port-forward pod/nvd-view-<id numbers> -n <namespace: for example nvd-analysis> 8082:8082

Now, service can be accessed over browser with url https://localhost:8082/v1/nvd_view

    
