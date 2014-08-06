# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 15:37:36 2014

@author: ayip
"""

import sys
import ga_api_v3_auth
from apiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError

def main(argv):
    service = ga_api_v3_auth.initialize_service()
    try:
        profile_id = get_first_profile_id(service)
        if profile_id:
            results = get_results(service,profile_id)
            print_results(results)
    except TypeError, error:
        print ('There was an error in constructing your query : %s' % error)
    except HttpError, error:
        print ('Arg, there was an API error : %s : %s' % (error.resp.status, error._get_reason()))
    except AccessTokenRefreshError:
        print ('The credentials have been revoked or expired, please re-run the application to re-authorize')

            
def get_first_profile_id(service):
    accounts = service.management().accounts().list().execute()
    if accounts.get('items'):
        firstAccountId = accounts.get('items')[0].get('id')
        webproperties = service.management().webproperties().list(accountId=firstAccountId).execute()
        
    if webproperties.get('items'):
        firstWebPropertyId = webproperties.get('items')[0].get('id')
        profiles = service.management().profiles().list(accountId=firstAccountId,webPropertyId=firstWebPropertyId).execute()
        
    if profiles.get('items'):
        return profiles.get('items')[0].get('id')
    return None

    
def get_results(service,profile_id):
    return service.data().ga().get(
        ids='ga:'+profile_id,
        start_date = '2013-12-01',
        end_date = '2013-12-01',
        dimensions = 'ga:source',
        metrics = 'ga:visits,ga:visitors,ga:percentNewVisits,ga:visitBounceRate,ga:transactions,ga:transactionRevenue').execute()

        
def print_results(results):
    if results:
        print 'First View (Profile): %s' % results.get('profileInfo').get('profileName')
        print results.get('rows')[0]
    else:
        print 'No results found'
        
        
if __name__ == '__main__':
    main(sys.argv)