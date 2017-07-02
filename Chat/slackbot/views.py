import os
import time
import random
import threading

from slackclient import SlackClient

from django.shortcuts import render
from user.models import User
from quiz.models import Quiz


# starterbot's ID
BOT_ID = "U632C7TJT"

# constants
AT_BOT = "<@" + BOT_ID + ">"
HELLO_COMMAND = ["hi", "hello", "하이", "ㅎㅇ", "안녕", "안녕하세요", "안뇽"]
HELLO_RETURN = "안녕하세요, OX퀴즈 챗봇입니다. OX퀴즈 하시겠어요? 전 아직 다른 일은 못해요."
NEGATIVE_RETURN = "유감이네요. 안녕히 가세요."
SORRY_RETURN = "미안해요.. 급하게 만든거라 다른 말은 대답 못해요. OX퀴즈나 풀어봅시다!"
GENERAL_POSITIVE_ANSWER_TEXT = ["ㅇ", "ㅇㅇ", "응", "그래", "알았어", "해봐"]
GENERAL_NEGATIVE_ANSWER_TEXT = ["ㄴ", "ㄴㄴ", "그만", "아니", "아니오", "아니요"]
OX_ANSWER_O = "O"
OX_ANSWER_X = "X"

# Slack clients
slack_client = SlackClient('xoxb-207080265639-svARVTOlxQ4450Ezon86fTt4')


def handle_command(command, channel, uid):

    # user check for context
    user = None
    result = User.checkUser(uid)
    if not result:
        user = User.createUser(uid)
    else:
        user = result

    # answer process
    if user.context == "answer_quiz":
        if command.lower() == "o" or command.lower() == "x":
            result, quiz_info = Quiz.checkCorrectAnswer(user.quizNum, command)
            user.nextQuiz()
            user.setContext("wait_quiz")
            response = result + "\n" + quiz_info + "\n" + "다음문제를 푸시겠습니까?"
        else:
            response = "O, X로 정답을 입력해 주세요."

        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
        return True

    elif user.context == "wait_quiz":
        if command in GENERAL_POSITIVE_ANSWER_TEXT:
            quiz = Quiz.getQuiz(user.quizNum)
            if quiz:
                user.setContext("answer_quiz")
                response = "다음 문제입니다." + "\n"
                response = response + quiz.quiz
            else:
                user.setContext("normal")
                user.setQuizNum(0)
                response = "더이상 풀 문제가 없습니다."

        elif command in GENERAL_NEGATIVE_ANSWER_TEXT:
            user.setContext("normal")
            response = NEGATIVE_RETURN
        else:
            response = SORRY_RETURN

        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
        return True

    else:
        if command in HELLO_COMMAND:
            response = HELLO_RETURN
        elif command in GENERAL_POSITIVE_ANSWER_TEXT:
            quiz = Quiz.getQuiz(user.quizNum)
            if quiz:
                user.setContext("answer_quiz")
                response = "OX 퀴즈를 시작하겠습니다." + "\n"
                response = response + quiz.quiz
            else:
                response = "더이상 풀 문제가 없습니다."
        else:
            response = SORRY_RETURN

        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
        return True


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                return output['text'].split(AT_BOT)[1].strip().lower(), output['channel'], output['user']
    return None, None, None


def slack_bot_starter():
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            read = slack_client.rtm_read()
            command, channel, uid = parse_slack_output(read)
            if command and channel and uid:
                handle_command(command, channel, uid)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")


# Django background must need linker view
def Linker(request):
    return render(request)


# start slackbot on background
t = threading.Thread(target=slack_bot_starter, args=())
t.daemon = True
t.start()