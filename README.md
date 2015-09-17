# graphiq-data-challenge
Veena Calambur
(vc233@cornell.edu)
Graphiq Data Challenge 

For the Graphiq Data Challenge, I got access to the Open Data Map datasets. I primarily worked with organizations.csv, that contained information such as the company name, URL, etc. 

I used the pandas package in Python to parse both organizations.csv and the sent companies_list.txt and filtered the organizations.csv to the companies that directly matched the the 64 sample companies given for the challenge, using regex and string parsing. 

From there I broke the challenge into two parts: one related with funding questions, and the other with investment questions. 

For the funding part, I located a specific URL: "https://www.crunchbase.com/organization/"+company_name+"/funding-rounds" which contained all funding information pertaining to a particular company. Using Python's Beautiful Soup, I parsed the HTML on this page and looked for the date and funding amount (located by their div names), and cleaned up the strings and processed the amounts and organized them by date. From there I accumulated them into a dictionary with the format: {'company name': [cumulative funding, change in funding between 2014-2015 ]}, which I could easily sort to obtain the top 10 companies in each category. 

I again performed a very similar process to for the questions related to investment categories, but had to use a slightly different URL and parse the HTML according to the table structure given for investments in total. 

If you have any other questions or concerns please let me know! 
