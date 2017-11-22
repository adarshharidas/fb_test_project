import json, requests
from django.http import HttpResponse
# from fb_app.utils import FacebookPageManager
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


class FacebookPageManager(object):
    """ Manages the Facebook Page"""
    API_ENDPOINT = 'https://graph.facebook.com/v2.10'

    def __init__(self, access_token):
        self.access_token = access_token

    def get_page_info(self):
        # returns the page information (first page) fb page owned by the user
        payload = {'access_token': self.access_token}
        url = '{}/me/accounts'.format(self.API_ENDPOINT)
        resp = requests.get(url, params = payload)
        data = json.loads(resp.text)
        if data.get('data'):
            page_info = data.get('data')[0]
            payload = {'access_token': self.access_token, 'fields' : 'single_line_address,phone,is_published,overall_star_rating,emails,about,location'}
            url = '{}/{}/'.format(self.API_ENDPOINT, page_info.get('id'))
            resp = requests.get(url, params = payload)
            data = json.loads(resp.text)
            data.update({'emails' :','.join(data.get('emails', []))})
            page_info.update(data)
            located_in_us = True if data.get('location',{}).get('country','').strip().lower() in ['united states', 'usa', 'us', 'united states of america'] else False
            page_info.update({'listed' : True, 'located_in_us' : located_in_us})
        else:
            page_info = {'listed' : False}
        print('Page get info response ', page_info)
        return page_info

    def update_page_info(self, data):
        # updates facebook page information
        print (data, "??????????????????????????????????????????????????")
        # location =  '{'+'"city": "{city}", "street": "{street}", "state": "{state}", "country": "{country}", "zip": "{zip}"'.format(city=data.get('city'), street=data.get('street'),  state=data.get('state'), country=data.get('country'), zip=data.get('zip')) + '}'
        # payload = {'access_token': data.get('access_token'), 'about' : data.get('about',''),'phone' : data.get('phone',''), 'emails' : '["{}",]'.format(data.get('emails')), 'location' : location}
        payload = {'access_token': data.get('access_token'), 'about' : data.get('about',''),'phone' : data.get('phone',''), 'emails' : '["{}",]'.format(data.get('emails'))}
        url = '{}/{}/'.format(self.API_ENDPOINT, data.get('id'))
        resp = requests.post(url, params = payload)
        print('Page update response ', resp.text)
        return json.loads(resp.text)


@login_required
def home(request):
    # Home page of the application
    social_user = request.user.social_auth.filter(provider='facebook', ).first() 
    access_token = social_user.extra_data['access_token']
    print (access_token, "????????????????????????????")
    fb_page_manager = FacebookPageManager(access_token)
    page_info = fb_page_manager.get_page_info()
    print (page_info, "PAGE INFOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO", type(page_info), ">>>>>>>>>>>>>>>>>>>")
    return render(request, 'fb/home.html', context=page_info)

@login_required
def update_page_info(request):
    # Updates the page information
    if request.method == 'POST':
        social_user = request.user.social_auth.filter(provider='facebook', ).first() 
        access_token = social_user.extra_data['access_token']
        fb_page_manager = FacebookPageManager(access_token)
        data = fb_page_manager.update_page_info(request.POST)
        error_user_msg = data.get('error').get('error_user_msg') if data.get('error') else ''
        return HttpResponse(json.dumps({'success' : 1 if data.get('success') else 2, 'eum' : error_user_msg}), content_type="application/json")
from django.shortcuts import render

# Create your views here.
