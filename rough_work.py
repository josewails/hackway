import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hackway.settings")
django.setup()

from binascii import hexlify

import json
import requests

from hway.models import CodingQuestion, FacebookUser, CodingResult

from hway.views import get_individual_score
from hway.bot_views import  done_with_quiz


#online
#page_access_token='EAAB9qLtZBAGoBALIZAUXOsrwZAQZAdnApZADJZCnwtkRdrLFr8ZBnQiNM7KhNGocTHA15qnKwzgbplmzWMPgR5wbW7lrxd5Qr6NXdbebdOUfSBBBlRxoYIupXKw5vAeqV4k1W4Dkcr5QMZB4q3fi3IobFEbrJaZAoUadFVsmzptRPYZBSDHBg0aPmA'

#local
page_access_token='EAACQBKzfE5YBAKdfQbkJOh585wDa5yPYsTqWy0wQbTWa6bpZCYyeqeaiMqYYBPhZCsiVVZCH08PA1OPPeUc88EUBjq3QulXw1vnDoxTDmL0ZBrPZBoomkPhZC9jCzKCXuUZBZCgck3RLTKvXw5D4iuCr5fNMziWfw7ZCL2hehN9ssyQZDZD'

def update_coding_question(question_id, source):
    current_question=CodingQuestion.objects.get(id=question_id)
    current_question.solution=source
    current_question.save()

#update_coding_question(3, source)

#add_coding_question(source=source, difficulty_level='intermediate')

profile_url='https://graph.facebook.com/v2.6/me/messenger_profile?access_token='+page_access_token

me_data={
    "whitelisted_domains":[
        "https://hackway.surge.sh",
        "https://8c8b16c4.ngrok.io"
  ]
}


profile_props_url="https://graph.facebook.com/v2.6/me/messenger_profile?fields=get_started&access_token="+page_access_token

#res=requests.post(url=profile_url, json=profile_data, headers=headers)

#res=requests.get(profile_props_url)3
#print(res.text)



#lang_checker=requests.get('http://api.hackerrank.com/checker/languages.json')
#print(lang_checker.json())

data={
        "code": "30",
        "name": "Python3",
        "questions": [
            {
                "question": "What statement do you use to remove the last element in a python list?",
                "difficulty_level": "simple",
                "answers": [
                    {
                        "answer": "pop",
                        "state": "1"
                    },
                    {
                        "answer": "remove",
                        "state": "2"
                    },
                    {
                        "answer": "get",
                        "state": "2"
                    },
                    {
                        "answer": "eliminate",
                        "state": "2"
                    }
                ]
            }
        ]
    }

persistent_menu_data={
  "persistent_menu":[
    {
      "locale":"default",
      "composer_input_disabled": True,
      "call_to_actions":[
          {
              "type": "postback",
              "title": '☱ Menu',
              "payload": "main_menu"
          },
        {
          "title":"Solve",
          "type":"nested",
          "call_to_actions":[
            {
              "title":" ⌨️ Programming Challenges",
              "type":"postback",
              "payload":"programming_questions"
            },
            {
              "title":"✍️ Multiple Answer Questions",
              "type":"postback",
              "payload":"programming_multiple_answer"
            }
          ]
        },
          {
              "title": "Ranking",
              "type": "nested",
              "call_to_actions": [
                  {
                      "title": "📊 My Progress",
                      "type": "web_url",
                      "url": 'https://hackway.surge.sh/individual_ranking',
                      'messenger_extensions': True,
                      'webview_height_ratio': 'tall'
                  },
                  {
                      "title": "👑 LeaderBoard",
                      "type": "web_url",
                      "url": 'https://hackway.surge.sh/full_ranking',
                      'messenger_extensions': True,
                      'webview_height_ratio': 'tall'
                  },
                  {
                      "title": "👨‍💻 👩‍💻Coding Ground",
                      "type": "web_url",
                      "url": 'https://hackway.surge.sh/coding_ground',
                      'messenger_extensions': False,
                      'webview_height_ratio': 'tall'
                  },
              ]
          }
      ]
    }
  ]
}

profile_data={
    "get_started":{
    "payload":"get_started"
  },
    'persistent_menu':persistent_menu_data['persistent_menu']

}

headers={
    "Content-Type": "application/json"
}

#res=requests.post(url=profile_url,json=profile_data, headers=headers)
#print(res.text)

#res=requests.post(url='http://localhost:8000/check_code', data=profile_data)
#print(res.text)

#done_with_quiz(messenger_id=r_data['messenger_id'])

"""
r_data={
    'messenger_id': '1528075240606741',
    'facebook_id': '1091795360951693',
    'question_id': 3
}"""


source="""prnt(5)"""
language_code='python'
d={
    'source_code': source,
    'language_used': language_code
}
#r=requests.post(url='http://localhost:8000/check_ground_code', data=d)
#print(r.text)
#
from hway.bot_views import send_code_segment_quiz
send_code_segment_quiz(messenger_id='1307518072599510', segment_id=1)
