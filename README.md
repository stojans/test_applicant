# test_applicant Odoo module

## Installation

1. Pull the code to the _server/odoo/addons/_ folder of your Odoo instalation
2. Restart the Odoo server
3. In Odoo web UI install Test Applicant Module

## Usage

After module install, users in the group Test Manager Group will be able to access _Settings > Test Applicant > Test Model_
Two cron jobs will be visible in the _Technical > Scheduled Actions_ menu: 
  Test Model: 'Confirmed' state update for confirmed states older than 30 minutes - every 5 minutes
  Test Model: 'reference_code' field reset - every 1 day

## Test Model Features

Adding and deleting entries with name, description, state, confirmation datetime (if state is confirmed), and reference code
State has possible values of 'Draft', 'Confirmed' and 'Done'
Reference codes are generated automatically, sequentially from TEST-0001
The two cron jobs are executed on module install and then every 5 minutes and 1 day, respectively
'Confirm' button in Test Model entries changes its state to 'Confirmed' and sets the date and time of the confirmation
