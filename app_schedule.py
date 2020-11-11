import time
import requests

file_path = "./data/sample_logs.log"
older_contents = ""

# in seconds
LOG_FORWARDER_INTERVAL = 5


def read_for_older_contents():
    global older_contents
    older_contents = (open(file_path, "r")).read()


def read_new_logs():
    global older_contents
    file = open(file_path, "r")
    new_contents = file.read()
    original_content = new_contents
    new_contents = new_contents.replace(older_contents, "")
    older_contents = original_content

    # check for new logs and forward to splunk
    if new_contents != "":
        print("sending logs")
        send_new_contents(new_contents)

    file.close()


def send_new_contents(new_contents):
    url = 'http://samplesplunk/logs'
    data_to_splunk = {'logs': new_contents}
    req_object = requests.post(url, data=data_to_splunk)
    print(req_object.text)


read_for_older_contents()

while True:
    read_new_logs()
    time.sleep(LOG_FORWARDER_INTERVAL)
