from flask import Flask, render_template, request, make_response, send_from_directory
import os
import sys
import pandas as pd
from pandas import DataFrame
import numpy as np
import json
import datetime
from datetime import datetime
import calendar
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities
import re
import time
from bs4 import BeautifulSoup

options = Options()
# options = webdriver.ChromeOptions()
options.add_argument("--disable-infobars")  
options.add_argument("--incognito")
# options.headless = True      
options.add_argument("headless") # Runs Chrome in headless mode.
# options.add_argument('--no-sandbox') # Bypass OS security model
options.add_argument('--disable-gpu')  # applicable to windows os only

# basepath="C:\\New Volume (D)\\Google Scholar Profile\\GUI\\template\\File\\"
ABDCpath="ABDC_2019.xlsx"
SCOPUSpath="SCOPUS_2018.xlsx"
chromepath="chromedriver.exe"

app = Flask(__name__, template_folder='template')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/") 
@app.route("/GS_Profile")
def GSProfile():
    return render_template('GS Profile.html')

@app.route('/getfile', methods=['GET','POST'])
def getfile():
    if request.method == 'POST':
        try:
            url = request.form['URL']
            ptype = request.form['Publication_Type']
            driver = webdriver.Chrome(chromepath, options=options)
            driver.delete_all_cookies()
            # clear_cache(driver)
            driver.get (url)
            # # driver.minimize_window()
            time.sleep(7)
            prev_paper_num_final = 0
            while (driver.find_element_by_xpath('//*[@id="gsc_bpf_more"]/span/span[2]')):
                driver.find_element_by_xpath('//*[@id="gsc_bpf_more"]/span/span[2]').click()
                time.sleep(5)
                src = driver.page_source
                soup = BeautifulSoup(src, 'html.parser')
                paper_num = soup.find("span", {"id":"gsc_a_nn"})
                paper_num = paper_num.text
                paper_num_final = int(str(paper_num).split("–")[1])
                if paper_num_final > prev_paper_num_final:
                    prev_paper_num_final = paper_num_final
                else:
                    break
            src = driver.page_source
            soup = BeautifulSoup(src, 'html.parser')
            job_elems = soup.find_all('tr', class_='gsc_a_tr')
            Scholar_Name = soup.find('title').text.split(' - ')[0]
            scholar_details=pd.DataFrame()
            for job_elem in job_elems:
                title_elem = job_elem.find('a', class_='gsc_a_at')
                name_elems = job_elem.find_all('div', class_='gs_gray')
                count=0
                for name_elem in name_elems:
                    if(count==0):
                        count+=1
                        authors=name_elem.text
                    else:
                        Publication_Name=name_elem.text
                year_elem = job_elem.find('span', class_='gs_oph')
                citation_elem = job_elem.find('a', class_='gsc_a_ac gs_ibl')    
                Publication_Name_words=Publication_Name.split(" ")
                conf_check = 0
                conf_word_list = ['conference', 'annual', 'meet', 'procedings', 'conf', 'conf.', 'proc.', 'proc']
                return render_template('Issue1.html')
                for word in Publication_Name_words:
                    if word.lower() in conf_word_list:
                        conf_check = 1     
                conf_name = ""        
                if conf_check == 1:
                    for word in Publication_Name_words:
                        if any(map(str.isdigit, word)):
                            continue
                        else:
                            conf_name = conf_name + word + " "
                    jname=conf_name        
                else:
                    final_Publication_Name = ""
                    for j in Publication_Name_words:
                        if any(map(str.isdigit, j)):
                            break
                        else:
                            final_Publication_Name = final_Publication_Name + j + " "
                    jname=(final_Publication_Name.split(",")[0]).strip()
                try:
                    if any(map(str.isdigit, citation_elem.text)):
                        cite=citation_elem.text
                    else:
                        cite="0"
                except:
                    cite="0"
                try:
                    p_year=year_elem.text.split(', ')[1]
                except:
                    p_year=""
                temp=pd.DataFrame({'Authors': [authors], 'Title': [title_elem.text], 'Publication_Name' : [jname], 'Citations' : [cite], 'Year':[p_year]})
                scholar_details=scholar_details.append(temp)
            return render_template('Issue1.html')
            scholar_details['Publication_Name']=scholar_details['Publication_Name'].str.replace("&", "and")
            scholar_details['Publication_Name']=scholar_details['Publication_Name'].str.replace(",","")
            scholar_details=scholar_details.where(scholar_details['Publication_Name']!="")
            scholar_details=scholar_details.dropna(how = 'all')
            scholar_details['Publication_Name']=scholar_details['Publication_Name'].str.title()
            df_Publication_Name=pd.DataFrame()
            df_citations=pd.DataFrame()
            dfd=pd.DataFrame()
            return render_template('Issue2.html')
            scholar_details['Citations']=scholar_details['Citations'].astype('int')
            df_Publication_Name=scholar_details.groupby(['Publication_Name'])['Citations'].count().reset_index(name='# of Articles')
            df_citations=scholar_details.groupby(['Publication_Name'])['Citations'].mean().reset_index(name='Avg Citations')
            dfd['Publication_Name']=df_Publication_Name['Publication_Name']
            dfd['# of Articles']=df_Publication_Name['# of Articles']
            dfd['Avg Citations']=df_citations['Avg Citations']
            ABDC=pd.read_excel(r""+ABDCpath)
            return render_template('Issue3.html')
            ABDC['Publication_Name']=ABDC['Publication_Name'].str.replace("&", "And")
            ABDC['Publication_Name']=ABDC['Publication_Name'].str.replace(",","")
            ABDC['Publication_Name']=ABDC['Publication_Name'].str.title()
            ABDC=ABDC[['Publication_Name','Year of Inception','Publication Rank (ABDC)']]
            final_df=pd.DataFrame()
            return render_template('Issue4.html')
            temp_df=pd.merge(dfd,ABDC,on='Publication_Name',how='left')
            SCOPUS=pd.read_excel(r""+SCOPUSpath)
            SCOPUS['Publication_Name']=SCOPUS['Publication_Name'].str.replace("&", "And")
            SCOPUS['Publication_Name']=SCOPUS['Publication_Name'].str.replace(",","")
            SCOPUS['Publication_Name']=SCOPUS['Publication_Name'].str.title()
            final_df=pd.merge(temp_df,SCOPUS,on='Publication_Name',how='left')
            return render_template('Issue5.html')
            final_df=final_df[['Publication_Name','Publisher','Year of Inception','Publication Rank (ABDC)','# of Articles','Avg Citations']]
            final_df.fillna('', inplace=True)
            final_df=final_df.sort_values(by = ['# of Articles','Avg Citations'], ascending=[False, False])
            final_df['Year of Inception'] = final_df['Year of Inception'].astype(str)
            final_df['Year of Inception'] = final_df['Year of Inception'].str.replace("\t","")
            final_df['Avg Citations']=final_df['Avg Citations'].astype('int')
            totalPublication=final_df['# of Articles'].sum()
            avgCitations=final_df['Avg Citations'].mean()
            avgCitations=int(avgCitations)
            return render_template('Issue6.html')
            return render_template('GS Profile.html', tables=[final_df.to_html(classes='data', header="true", index=False)], CNAME=Scholar_Name, TPUB=totalPublication, AVGCITE=avgCitations)
        except:
            return render_template('Issue.html')
    else:
        return render_template('GS Profile.html')
if __name__ == "__main__":
    app.run(debug=True, host = '0.0.0.0')
