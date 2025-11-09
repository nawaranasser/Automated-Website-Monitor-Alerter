# monitor.py
import requests
import time
import config
from email_sender import send_alert_email
from datetime import datetime


# # The website we want to monitor
# URL =  "https://www.google.com"  # A reliable test URL that always returns "200 OK"
# # URL2 = "https://httpbin.org/status/200"  # another url to test with
# TIMEOUT = 5  # seconds
# SLOW_THRESHOLD = 2.0  # Website is slow if response time > 2 seconds
# #change SLOW_THRESHOLD = 0.1 (very low) to test what happend when it be slow


def log_event(event_message):
    """Log events to a file with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {event_message}\n"
    
    with open("monitor.log", "a") as log_file:
        log_file.write(log_entry)
    
    print(log_entry.strip())  # Also print to console



def check_website():
    """
    This function checks the status of the website and measures its response time.
    """
    try:
        # Record the start time before making the request
        start_time = time.time()

        # Send a GET request to the website.
        # 'timeout=5' means if the website doesn't respond in 5 seconds, it's considered an error.
        response = requests.get(config.URL, timeout=config.TIMEOUT)

        # Calculate the response time in seconds
        response_time = time.time() - start_time

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:

            if response_time > config.SLOW_THRESHOLD:
                
                alert_msg = f"🚨 Website is SLOW\nURL: {config.URL}\nResponse Time: {response_time:.2f}s\nThreshold: {config.SLOW_THRESHOLD}s\nTime: {time.ctime()}"   
                # print(alert_msg)
                log_event(f"SLOW - Response Time: {response_time:.2f}s")
                send_alert_email("🚨 Website Performance Alert", alert_msg)
                return False, response_time, alert_msg
            
            
            else:
                # print(f"✅ Website is HEALTHY & UP. Response Time: {response_time:.2f} seconds")
                log_event(f"HEALTHY - Response Time: {response_time:.2f}s")
                return True, response_time, None
            

        else:
            # The website responded, but with a bad status code (e.g., 404, 500)
            alert_msg = f"🚨 Website is DOWN\nURL: {config.URL}\nStatus Code: {response.status_code}\nTime: {time.ctime()}"
            # print(alert_msg)
            log_event(f"DOWN - Status Code: {response.status_code}")
            # Send email alert for down website
            send_alert_email("🚨 Website Down Alert", alert_msg)
            return False, response_time, alert_msg

    except requests.exceptions.RequestException as e:
        # This block runs if the request completely fails (e.g., no internet, domain not found, timeout)
        alert_msg = f"🚨 Website is UNREACHABLE\nURL: {config.URL}\nError: {e}\nTime: {time.ctime()}"
        # print(alert_msg)
        log_event(f"UNREACHABLE - Error: {e}")
        # Send email alert for unreachable website
        send_alert_email("🚨 Website Unreachable Alert", alert_msg)
        return False, None, alert_msg

# This is the standard Python way to say "run this code if the script is executed directly"
if __name__ == "__main__":
    print("🚀 Starting website health check...")
    is_healthy, response_time, alert_message = check_website()
    
    # Print summary for debugging
    # if alert_message:
    #     print(f"🔔 ALERT TRIGGERED: {alert_message}")
    # else:
    #     print("✅ No issues detected.")
    if not is_healthy:
        log_event(f"Alert processed: {alert_message.split(chr(10))[0]}")  # First line only
        log_event("---")
    else:
        log_event("No issues detected")
        log_event("---")