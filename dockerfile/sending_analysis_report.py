import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
   
def email_report(opened_pull_request_report,closed_pull_request_report,reposistry):	
	fromaddr = input("Enter sender mail address: ")
	toaddr = input("Enter receiver mail address: ")
	passwd = input("Enter sender's App password: ")

	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Final Analysis Report of {} Pull requests from last week".format(reposistry)

	body = """Weekly Pull Requests Report
	
Opened Pull Request Report 
 {}
Closed Pull Request Report :
 {} """.format(opened_pull_request_report,closed_pull_request_report)

	msg.attach(MIMEText(body, 'plain'))
	 
	filename = "analysis_report.json"
	attachment = open("./analysis_report.json", "rb")
	  
	p = MIMEBase('application', 'octet-stream')
	p.set_payload((attachment).read())
	encoders.encode_base64(p)  
	p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
	msg.attach(p)

	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.starttls()
	s.login(fromaddr,passwd)

	text = msg.as_string()

	s.sendmail(fromaddr, toaddr, text)

	s.quit()
