# 스니펫
Snippets는 구글이 사내에서 운영하는 업무 공유용 이메일 시스템입니다.

### 스니펫 동작 방식

매주, 스니펫 시스템으로부터 리마인더 이메일이 발송됩니다.
사용자들은 지난 주에 무엇을 했는지 여기에 답변으로 보낼 수 있어요.
웹을 통해 다른 사용자들을 follow 할 수 있습니다.
태그 기능도 있어서 자기 자신을 태그에 할당하고, 이렇게 생긴 태그 역시 follow 할 수 있습니다.
그러고나면 매주 월요일에 follow 한 태그나 사용자에 대한 다이제스트 메일을 받게 됩니다.
추가로 각 사용자들의 아카이브도 웹에서 볼 수 있어요.

**fork 후 수정 내용은 크게 없어요**

* 타임존을 서울/아시아로 변경
* 수정할 부분 FIX ME로 표시
* 가입 계정 소문자 변환
* 서명, 답변 패턴 추가

### 사용하기
1. git clone git@github.com:curioe/snippets.git
2. [구글앱엔진](https://appengine.google.com) 에서 새 앱을 생성합니다.
3. 소스를 생성한 이름에 맞게 수정합니다. ('FIX ME'로 검색하세요)
4. 구글앱엔진 런처를 실행하여, 또는 커맨드로 배포하면 완료됩니다.
5. 웹 - {앱명}.appspot.com 과, 메일 - snippets@{앱명}.appsotmail.com 을 통해 스니펫을 시작하세요. :)

### 나에게 맞게 수정
* trim될 서명, 답변 패턴을 정규식으로 추가 -> receive_email.py
* 리마인더/다이제스트 메일 발송 시각 변경 -> cron.yaml




-----
# Original README
Folks who worked at Google may miss snippets at their current
employers. Help is at hand.

Every week, the system emails out a reminder email. Users can reply to
it with what they did that week. Users can follow other users via the
web, as well as following tags, and assigning tags to themselves. All
content matching the tags they follow will be mailed to them in a
digest every Monday afternoon. In addition, archives for each user and
the most recent data for each tag are visible on the web.

It was hard to make this totally portable. You'll probably want to
fork and change the application name and hardcoded email addresses,
creating your own application on app engine with authentication
restricted to your custom domain. I would love patches to core
functionality, though.

Little attention has been paid to making this particularly scalable,
but it should work for any small or medium company.