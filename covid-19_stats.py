#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup as bs
import json
import pprint
from termcolor import colored
import sys
import datetime
now = datetime.datetime.now()
print("Current date and time: " + str(now.strftime("%Y-%m-%d %H:%M:%S")))
print("")

#https://www.worldometers.info/world-population/population-by-country/

color=False

if len(sys.argv) > 1:
	if sys.argv[1] == "--color":
		color=True

def percentage(part, whole):
  return round(100 * float(part)/float(whole),4)

session = requests.Session()
headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0","Connection":"close","Accept-Language":"en-US,en;q=0.5","Accept-Encoding":"gzip, deflate"}
response = session.get("http://topic.newsbreak.com/covid-19.html", headers=headers)
#print("Status code:   %i" % response.status_code)
#print("Response body: %s" % response.content)
soup  = bs(response.content,'html.parser')
scriptid = soup.find("script", {"id": "__NEXT_DATA__"}).text.encode('utf-8')

session = requests.Session()
headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0","Connection":"close","Accept-Language":"en-US,en;q=0.5","Accept-Encoding":"gzip, deflate"}
response = session.get("https://www.livepopulation.com/", headers=headers)
#print("Status code:   %i" % response.status_code)
#print("Response body: %s" % response.content)
world = bs(response.content,'html.parser')
worldpop = int(world.find("td", {"class": "current-population"}).text.encode('utf-8').replace(",",""))

print("World Population: " + str(worldpop))
print("")

dict = json.loads(scriptid)

#print(dict["props"]["pageProps"]["data"]["global_stats"][0:5])
num=20
top=dict["props"]["pageProps"]["data"]["global_stats"][0:num]

infected=int(dict["props"]["pageProps"]["data"]["global"]["f"])
recovered=int(dict["props"]["pageProps"]["data"]["global"]["r"])
dead=int(dict["props"]["pageProps"]["data"]["global"]["d"])

print("Infected: " + str(infected))
print("Recovered: " + str(recovered))
print("Dead: " + str(dead))

death_rate=percentage(dead,infected)
global_infection=percentage(infected,worldpop)
global_death_percent=percentage(dead,worldpop)
global_recovery=percentage(recovered,infected)
global_risk=percentage(infected-dead-recovered,infected)

print("Global Infected Death Rate: " + str(death_rate) +"%")
print("Global Infection Percentage: " + str(global_infection) + "%")
print("Global Population Death Percentage: " + str(global_death_percent) + "%")
print("Global Recovery Percentage: " + str(global_recovery) + "%")
print("Global Infected Still at Risk: " + str(global_risk) + "%")
print("")
print("Top " +str(num)+" Infected Countries:")
for country in top:
	name=country["tl"]
	ci=country["f"]
	cd=country["d"]
	cr=country["r"]
	crp=percentage(cr,ci)
	cdp=percentage(cd,ci)
	csp=percentage(ci-cd-cr,ci)

	if color:
		if crp >= global_recovery:
			crp=colored(str("%.4f"%crp)+"%",'green')
		else:
			crp=colored(str("%.4f"%crp)+"%",'yellow')

		if cdp > death_rate:
			cdp=colored(str("%.4f"%cdp)+"%",'red')
		else:
			cdp=colored(str("%.4f"%cdp)+"%",'yellow')

		if csp != 0.0:
			if csp > global_risk:
				csp=colored(str("%.4f"%csp)+"%",'red')
			else:
				csp=colored(str("%.4f"%csp)+"%",'yellow')
		else:
			csp=colored(str("%.4f"%csp)+"%",'green')
	else:
		crp=str("%.4f"%crp)+"%"
		cdp=str("%.4f"%cdp)+"%"
		csp=str("%.4f"%csp)+"%"

	if color:
		print("Country: %-20s Infected: %-10s Dead: %-10s Recovered: %-10s Death Rate: %-20s Recovery Rate: %-20s At Risk: %-20s" % (str(name),str(ci),str(cd),str(cr),str(cdp),str(crp),str(csp)))
		print("")
	else:
		print("Country: %-20s Infected: %-10s Dead: %-10s Recovered: %-10s Death Rate: %-9s Recovery Rate: %-9s At Risk: %-9s" % (str(name),str(ci),str(cd),str(cr),str(cdp),str(crp),str(csp)))
		print("")
