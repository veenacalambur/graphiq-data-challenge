#author: Veena Calambur 
#Graphiq Data Challenge


import os
import pandas as pd
import urllib
from bs4 import BeautifulSoup
import re
import datetime as dt
import operator

#os.chdir("/Users/VeenaCalambur/OneDrive/odm")

#read in organizations.csv, and grab the URLs and company names for each company
org = pd.read_csv('organizations.csv')
names = org['name']

#Convert names into an array of words (i.e. Omidyar Network = [Omidyar , Network])
names = names.str.findall('[A-Z][^A-Z]*')

#get 64 company names from company list and clean up strings and similarly convert it to an array of words 
#(i.e. omidyar-network = [omidyar, network])
sample_64 = pd.read_table('company_list.txt', header = None, names = ["company"])
sample_64["company"] = sample_64["company"].str.strip().split('-')
sample_64["company"] = sample_64["company"].str.split('-')


indices = []
temp_check = []

for n in range (len(names)):
    try:
        names[n] = [x.strip() for x in names[n] ]
        names[n] = [x.lower() for x in names[n] ]
        for s in sample_64["company"]:     
            if set(names[n]) == set(s) and names[n] not in temp_check : 
                indices.append(n)
                temp_check.append(names[n])
    except:
        continue

#get the final list of company names which matched the company_list.txt file (WARNING: some missin)
final_companies = names[indices]
final_urls = url[indices]
#CHALLENGE QUESTIONS 1 & 2: FUNDING INFO 
funding_by_company = {}         
for c in final_companies : 
    co = c[0].replace(" ", "-")
    url = "https://www.crunchbase.com/organization/"+co+"/funding-rounds"
    f = urllib.urlopen(url)
	html = f.read() 
	soup = BeautifulSoup(html, 'html.parser')
	fund_html = soup.findAll(True, {"class":["funding_amount", "date"]})

	funding_info = {};
	amt = "";
	funding_by_company = {} 
	#no funding information available 
	if(len(fund_html) ==0): 
		funding_by_company[co] = [0, 0]
	else: 
		for i in xrange(0, len(fund_html), 2):

		    amt = fund_html[i].get_text()
		    dte = fund_html[i+1].get_text()
		    fund_date = dt.datetime.strptime(dte, '%B %d, %Y').strftime('%Y')
		    val = re.split("([a-zA-Z])",amt[1:])

		    fund_inst = convert_dollar(val)

		    if fund_date in funding_info.keys():
	        	#add to that year's amt: 
	        	fund_inst += funding_info[fund_date]   

	    	funding_info[fund_date] = fund_inst  

		#fill in cumulative funding amt per person
		cum_fund = sum([i for i in funding_info.values()])

		#find change in fund between 2015 and 2014 
		delta_14_15 = 0
		if(('2015' in funding_info.keys())): 
			if(('2014') in funding_info.keys()):
				delta_14_15 = funding_info['2015'] - funding_info['2014'] 
			else: #company just got funding in 2015 so 2014 funding = 0 
				delta_14_15 = funding_info['2015']

		funding_by_company[co] = [cum_fund, delta_14_15]

#find top 10 by cumulative funding 
cum_fundings = sorted(funding_by_company.items(), key=lambda i: i[1][0], reverse=True)
top_companies_cum_findings = [i[0] for i in cum_findings][:10]
print (top_companies_cum_findings)


#find top 10 by change cumulative funding between 2014 and 2015
delta_cum_findings = sorted(funding_by_company.items(), key=lambda i: i[1][1], reverse=True)
top_companies_delta_cum_findings = [i[0] for i in delta_cum_findings][:10]
print(top_companies_delta_cum_findings)


########################################################


#sort through data structure to obtain the answers: 
#CHALLENGE QUESTIONS 3 & 4: FUNDING INFO 
investment_by_company = {} 

#loop through each of the matched companies and get HTML their crunchbase URL
#parse it using Beautiful Soup: 

for co in final_companies: 
    c = co[0].replace(" ", "-")
    url_inv = "https://www.crunchbase.com/organization/"+c
    f = urllib.urlopen(url)
	html_inv = f.read() 
	soup_inv = BeautifulSoup(html_inv, 'html.parser')
	#investment tables are labeled by odd/even rows: 
	inv_html = soup_inv.findAll("tr", { "class" : ["odd", "even"] })

	investing_info = {};

	#no investment information available
	if(len(inv_html) ==0):
		investment_by_company[c] = [0, 0]
	else: 

		for i in xrange(0, len(inv_html)):

			#parse the HTML to get the investment by date and amount 
			inv_breakdown = str(inv_html[i]).split("<td>")
			inv_dte = inv_breakdown[1][:-5]

			inv_date = dt.datetime.strptime(inv_dte, '%b %d, %Y').strftime('%Y')

			val_inv = re.split('(\s)', inv_breakdown[3])[0]
			val = re.split("([a-zA-Z])",val_inv[1:])
			inv_inst = convert_dollar(val)
			    
			if inv_date in investing_info.keys(): #add to that year's amt: 
				inv_inst += investing_info[inv_date]   
			investing_info[inv_date] = inv_inst

		#fill in cumulative investment amt per company
		cum_inv = sum(investing_info.values())

		#find change in investments between 2015 and 2014 
        inv_delta_14_15 = 0
        if(('2015' in investing_info.keys())): 
            if(('2014') in investing_info.keys()):
                inv_delta_14_15 = investing_info['2015'] - investing_info['2014'] 
            else: #company just invested in 2015 so 2014 funding = 0 
                inv_delta_14_15 = investing_info['2015']

        investment_by_company[c] = [cum_inv, inv_delta_14_15]

#find top 10 by cumulative investments 
cum_investments = sorted(investment_by_company.items(), key=lambda i: i[1][0], reverse=True)
top_companies_cum_investments = [i[0] for i in cum_investments][:10]
print (top_companies_cum_investments)


#find top 10 by change cumulative ivestments  between 2014 and 2015
delta_cum_investments = sorted(funding_by_company.items(), key=lambda i: i[1][1], reverse=True)
top_companies_delta_cum_investments = [i[0] for i in delta_cum_findings][:10]
print(top_companies_delta_cum_investments)


#Helper function to convert text amount on the website to a dollar amount 
def convert_dollar(val_array): 
	try:
		val_num = float(val_array[0])

	    if val_array[1] == "B":
	        fund_inst = val_num * 10**9
	    elif val_array[1] == "M":
	        fund_inst = val_num * 10**6
	    elif val[1] == "k":
	        fund_inst = val_num * 10**3
	    else: 
	        fund_inst = val_num
	    return(fund_inst)
	except:
		#non valid array of dollar amount was given, just return 0 
		return(0)





