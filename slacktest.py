# -*- coding:utf-8 -*-
from slacker import Slacker

token = 'xoxb-207080265639-42Nsl27M2iv6N2oYw3RXrXEL' # test_bot의 토큰

slack = Slacker(token)

# 단문 메시지 보내기
slack.chat.post_message('#test', '안녕하세요. Test_Bot입니다.') # test 채널에 메시지를 보낸다.