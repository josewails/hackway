import requests
from YamJam import yamjam



config = yamjam()['hackway']
page_access_token = config['PAGE_ACCESS_TOKEN']

profile_url = 'https://graph.facebook.com/v2.6/me/messenger_profile?access_token='+page_access_token


data = {
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

persistent_menu_data = {
  "persistent_menu": [
    {
      "locale": "default",
      "composer_input_disabled": True,
      "call_to_actions": [
          {
              "type": "postback",
              "title": '☱ Menu',
              "payload": "main_menu"
          },
          {
              "title": "Solve",
              "type": "nested",
              "call_to_actions": [
                  {
                      "title": " ⌨️ Programming Challenges",
                      "type": "postback",
                      "payload": "programming_questions"
            },
                  {
                      "title": "✍️ Multiple Answer Questions",
                      "type": "postback",
              "payload": "programming_multiple_answer"
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
    "get_started": {
    "payload": "get_started"
  },

    "whitelisted_domains": [
        "https://hackway.surge.sh",
        "https://bec34d1e.ngrok.io"
  ],

    'persistent_menu': persistent_menu_data['persistent_menu']

}

headers={
    "Content-Type": "application/json"
}

res = requests.post(url=profile_url,json=profile_data, headers=headers)
print(res.json())
