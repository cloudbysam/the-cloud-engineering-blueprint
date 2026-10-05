#!/bin/bash

URL="http://127.0.0.1:8080/"

# Run curl silently, fetch HTTP status code, and capture curl's exit code
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 --max-time 3 "$URL")
CURL_EXIT_CODE=$?

# Only mark as UP if curl succeeded (exit code 0) AND HTTP status is 200
if [ $CURL_EXIT_CODE -eq 0 ] && [ "$HTTP_STATUS" = "200" ]; then
    echo "$(date): [OK] Server is UP (Status 200)"
else
    echo "$(date): [FAIL] Server is DOWN or unresponsive (HTTP Status: '${HTTP_STATUS}', Curl Exit Code: ${CURL_EXIT_CODE}). Restarting..."
    systemctl restart http-server.service
fi

# make it executable: chmod +x /path/05-server-uptime-tests/health-check.sh