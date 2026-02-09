# URL Health Check

## Project Description
This project provides a simple script to check the health of websites listed in a CSV file. It logs the status, response time, and timestamp for each URL directly in the CSV, making it easy to monitor site availability without relying on third-party monitoring applications.

## Usage

- Add your website URLs to `websites_url.csv` under the `website` column.
- Run the script:
	```
	python healthcheck.py websites_url.csv
	```
- The script will update the CSV with health status, response time, and check timestamp.

### Email Report
- To send an email report after health checks, use:
	```
	python healthcheck.py websites_url.csv --send-email
	```
- The script uses placeholder SMTP and email details. Update the sender, recipient, SMTP server, port, username, and password in `healthcheck.py` before using in production.


## Cron Job Setup
- Schedule the script to run at regular intervals using Windows Task Scheduler or a cron job (on Linux/macOS).
- Example (Linux):
	```
	0 * * * * /usr/bin/python3 /path/to/healthcheck.py /path/to/websites_url.csv
	```
- This checks URLs every hour.

## Dev Environment Benefits
- No dependency on external monitoring tools.
- Quick feedback for developers on site uptime.
- Easily extensible for custom checks.
 - Email reporting for easy sharing and alerting.
