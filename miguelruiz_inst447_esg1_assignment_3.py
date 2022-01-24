import re, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

f = open('email_log.txt', 'r')
text = f.read()
#print(text)
f.close()


# use regular expressions to select key elements
# create a data frame with this information

serverlist = re.finditer("(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2}).\d+ \d{5} .+:? \` (?P<IP>\d+.\d+.\d+.\d+).+\<(?P<email>\w+@?.+[.com]?)\>\s+\w{5}\s+\d{3}\s+(.+)(?P<reason>msg denied before queued+)",text)
newList = []
for things in serverlist:
    newList.append({'Date':things['date'],'Time':things['time'],'IP Address':things['IP'],'Email':things['email'],'Reason':things['reason']})
df = pd.DataFrame(newList)

f = open('raw_email.txt', 'r')
text = f.read()
print(text)
f.close()

# Get the email addresses of the lists this was sent to using regular expressions

lists = "To:\s\".+\"\s\<(.+@\w{8}\.\w{4}\.\w{3})\>,\s.+\s\<(.+@\w{8}\.\w{4}\.\w{3})\>"
elist = re.findall(lists,text)

# Get the name of the sender using regular expressions

senderName = "From:\s\"(.+)\""
sMatch = re.search(senderName,text)
sMatch.group(1)

# Get the email of the sender using regular expressions

sender = "Sender:\s.+\s\<(.+@\w{8}\.\w{4}\.\w{3})\>"
slist = re.search(sender,text)
slist.group(1)

# Find all the IP addresses using regular expressions

IP = "\d+\.\d+\.\d+\.\d+"
ipMatch = re.findall(IP, text)

# I created a minimized version of the original file.
f = open('fraudulent_emails_minimized.txt', 'r', encoding="ISO-8859-1")
text = f.read()
print(text)
f.close()

# Get the "Subject:" of the emails using regular expressions and put them in a dataframe
# remove any that do not contain any text

subj = "Subject:\s(.+)"
subMatch = re.findall(subj,text)
subMatch
subjDF = pd.DataFrame({"subject":subMatch})

# Write an aggregation to see the top 5 subject lines by count

subjDF.value_counts().nlargest(5)

# Get the "From:" of the emails using regular expressions and put the emails in a dataframe
# remove any that do not contain any text
regex1 = "From:\s\".+\".+\<(.+@.+)\>"
regex2 = "From:\s(\w+@.+)"

elist = []
for exp in [regex1,regex2]:
    fromMatch = re.finditer(exp,text)
    for words in fromMatch:
        emails = words.groups(1)
        elist.append(emails[0])
        emailDF = pd.DataFrame({'Emails':elist})

# Write an aggregation to see the top 5 "From:" by count

emailDF.value_counts().nlargest(5)

# Get the "Date:" of the emails using regular expressions and put them in a dataframe
# Remove any rows without a date
# Remove any that are before 1998 (you'll see some from 1980...obvious errors)

regex1 = "Date:\s+(\w{3}),\s\d{1,2}\s\w{3}\s(\d{4})"
regex2 = "Date:(\w{3}),\s+\d{1,2}\s\w{3}\s(\d{4})"

dlist = []
dayslist = []
for exp in [regex1,regex2]:
    fromMatch = re.finditer(exp,text)
    for words in fromMatch:
        year = words.groups(2)
        day = words.groups(1)
        date = words.group(0)
        if int(year[1]) < 1998:
            continue
        else:
            dlist.append(date[5:])
            dayslist.append(day[0])

datesDF = pd.DataFrame({'Dates':dlist})

# Create a graph by day of week when the email was sent
# Does there seem to be a difference in terms of the day of the week a fraudulent email was sent?

plt.hist(dayslist,bins=15);

# The frequency in which fraudulent emails are sent look higher during the weekdays compared to the weekend.