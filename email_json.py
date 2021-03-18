# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 12:18:57 2021

@author: sayers
"""
from src.admin import write_json, newest, rehead, colclean
import pandas as pd
import os


#get e-mail data  - This file came from personal query 'HR_REPORTS_EMAILS_ALL' in HCM reporting instance
def getemails(filefolder):
    path=filefolder
    fname='HR_REPORTS_EMAIL'       #latest data from cunyfirst with e-mails
    emails=colclean(rehead(pd.read_excel(newest(path,fname)),1))
    #do some operations here, shane
    return(emails)

# the email list returned is dirty data and is in the wrong shape. Time to fix it
def cleanemail(df):
    tuplelist=list(df[['id', 'email','type']].dropna(how="any").itertuples(index=False,name=None))
    tupledict={}
    for tupleobj in tuplelist:
        tupledict.update({f'{tupleobj[0]}_{tupleobj[2]}':tupleobj[1]})
    return(tupledict)
    
#we want dictionaries, not dataframes
def write_emails(tupledict,fileloc):
    write_json(tupledict,fileloc)

def emailcycle(fileloc1,fileloc2):
    tupledict=cleanemail(getemails(fileloc1))
    write_emails(tupledict,fileloc2)

def unpack(fileloc1,fileloc2):
    emails=getemails(fileloc1)
    emails=emails[['id','email','type']].drop_duplicates()
    emails=pd.pivot(emails, values='email',index='id',columns='type').fillna('')[['BUSN', 'CAMP', 'DORM', 'HOME', 'OTHR']]
    emails.to_excel(os.path.join(fileloc2,'all_emails_report.xls'))
    
if __name__=="__main__":
    unpack('s://downloads','Y://current data//lookup tables')
    emailcycle('s://downloads','Y://Program Data//emails')