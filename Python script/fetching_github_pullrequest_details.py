import requests
import json
from datetime import datetime, timedelta
import sending_analysis_report as sar

results=[]
email_body=[]

#Calculate the time difference between current time and last pull request
def timetest(pull_request_created_date):
	pull_request_created_date=pull_request_created_date.split("T")[0]
	pull_request_created_date=datetime.strptime(pull_request_created_date,"%Y-%m-%d")
	current_date = str(datetime.now()).split(" ")[0]
	current_date =datetime.strptime(current_date,"%Y-%m-%d")
	delta=current_date-pull_request_created_date
	return(delta.days)

#fetch the PR statistics
def fetch_requests(state,reposistry):
	count=1
	pull_count=0
	Flag=True
	print("Fetching {} pull request details ....".format(state))
	pull_request_url = "https://api.github.com/repos/{}/pulls?page={}&per_page=100&state={}".format(reposistry,count,state)
	while(Flag==True):	
		fetch = requests.get(pull_request_url)
		data = json.loads(fetch.text)
		for i in range(len(data)):
			lastPRcreationTime=timetest(data[i]['created_at'])
			if lastPRcreationTime in range(0,8):
				pull_count+=1
				pull_request_num=data[i]['number']
				pull_request_by=data[i]['user']['login']
				pull_request_created_at=data[i]['created_at']
				pull_request_closed_at=data[i]['closed_at']
				results.append({"pull_request_num": pull_request_num,
						"pull_request_raised_by": pull_request_by,
						"state_of_pull_request": state,
						"pull_request_created_at": pull_request_created_at,
						"pull_request_closed_at": pull_request_closed_at
					     })
			else:
				return pull_count
		
		if(len(data)==100):
			count+=1
			pull_request_url = "https://api.github.com/repos/pulls?page={}&per_page=100&state={}".format(reposistry,count,state)	
		else:
			return pull_count

states=['open','close']
reposistry=input("Enter username and reposistry (username/reposistry) : ")
for state in states:
	pull_count=fetch_requests(state,reposistry)
	email_body.append("Total no of {} pulls are: {}".format(state,pull_count))
	
with open('analysis_report.json','w+') as file:
	json.dump(results, file, indent = 2)
	
sar.email_report(email_body[0],email_body[1],reposistry)
