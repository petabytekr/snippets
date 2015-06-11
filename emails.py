# -*- coding: utf-8 -*-
import logging
import datetime

from google.appengine.api import mail
from google.appengine.api import taskqueue
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from dateutil import *
from model import *

REMINDER = """
금주에도 수고하셨습니다.
회신으로 주간 작업내용을 입력해주세요. ;)

< 한일 >
- 

< 할일 및 예정일정 >
- 

< 이슈사항 >
- 


* 참고 - 금요일의 15분(Practice the Friday 15)
1. 첫 번째 작업은 이번 주의 내 계획을 돌아보는 것이다.
계획을 돌아보면, 그토록 아름답게 조직되어 시작했던 내 계획이 얼마나 엉망으로 실행되었는지가 보인다. 나는 많은 일을 했지만, 대개 내 할 일 목록은 한 주를 시작했을 때보다 더 길어져있다. 이 목록을 보고, 나는 내가 몇 분 이내로 끝내버릴 수 있는 작업들을 골라낸다. 때로는 못 받은 전화 다시 걸기, 요금 내기, 블로그 글 간단히 수정 같은 간단한 일들이 목록에 남아있기 때문이다. 그것들을 끝내버린다.

2. 두 번째 작업은, 그 목록에서 '다음 주로 넘길 일', '다른 사람에게 맡길 일', 또는 '하지 않을 일'을 나누는 것이다. 다음으로 넘기거나, 남에게 넘기거나, 버린다.

3. 세 번째 작업은, 다음 주를 위한 새 계획을 세우는 것이다.
우리가 계획을 세울 때 종종 하는 실수는, 우리가 하고 싶은 모든 일을 다 집어넣는 것이다. 그러나 우리의 기대치는 언제나 너무 높다. 나는 보통 사람들에게 다음 주에 꼭 해야 할 중요한 일 10여가지만 쓰라고 한다. (그걸 filght plan이라고 부른다) 파일럿처럼, 이제 나는 내가 어디에 착륙해야 할지 안다. 금요일이면 그 10여가지 목록은 완수되어있어야 한다.

4. 마지막 작업은 내 공간을 정리하는 것이다.
잡동사니를 치운다. 어지러진 걸 버린다. 포스트잇, 펠트 펜, 그냥 펜, 연필, 기타등등을 정리한다. 내가 다음 주에 돌아왔을 때, 정돈된 책상은 성공한 듯한 기분을 든다. 나는 잡동사니에 둘러쌓여있을 때면 성공한 기분이 절대 안 든다. 왜냐하면, 어지러진 책상은 집중에 방해될 뿐만 아니라(잡동사니를 보고, 그것에 대해 생각한다), 내가 무언가 완료하지 못했다는 느낌을 주기 때문이다.

"""

class ReminderEmail(webapp.RequestHandler):
    def get(self):
        all_users = User.all().filter("enabled =", True).fetch(500)
        for user in all_users:
            # TODO: Check if one has already been submitted for this period.
            taskqueue.add(url='/onereminder', params={'email': user.email})


class OneReminderEmail(webapp.RequestHandler):
    def post(self):
        mail.send_mail(sender="snippets <snippets@gcentask.appspotmail.com>", # FIX ME
                       to=self.request.get('email'),
                       subject=("주간업무 기록시간입니다. " + datetime.datetime.now().strftime('%Y.%m.%d') + " #gcentask"),
                       body=REMINDER)

    def get(self):
        post(self)

class DigestEmail(webapp.RequestHandler):
    def get(self):
        all_users = User.all().filter("enabled =", True).fetch(500)
        for user in all_users:
            taskqueue.add(url='/onedigest', params={'email': user.email})
            

class OneDigestEmail(webapp.RequestHandler):
    def __send_mail(self, recipient, body):
        mail.send_mail(sender="snippets <snippets@gcentask.appspotmail.com>", # FIX ME
                       to=recipient,
                       subject=("주간업무 종합 " + datetime.datetime.now().strftime('%Y.%m.%d') + " #gcentask"),
                       body=body)

    def __snippet_to_text(self, snippet):
        divider = '-' * 30
        return '%s\n%s\n%s' % (snippet.user.pretty_name(), divider, snippet.text)

    def get(self):
        post(self)

    def post(self):
        user = user_from_email(self.request.get('email'))
        d = date_for_retrieval()
        all_snippets = Snippet.all().filter("date =", d).fetch(500)
        all_users = User.all().fetch(500)
        following = compute_following(user, all_users)
        logging.info(all_snippets)
        body = '\n\n\n'.join([self.__snippet_to_text(s) for s in all_snippets if s.user.email in following])
        if body:
            self.__send_mail(user.email, 'https://gcentask.appspot.com\n\n' + body) # FIX ME
        else:
            logging.info(user.email + ' not following anybody.')
