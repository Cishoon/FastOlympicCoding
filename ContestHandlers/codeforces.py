import urllib
import urllib.request
import re
import sublime
import sublime_plugin
import codecs
import os
from bs4 import BeautifulSoup
import requests


test_tokens = ['<div class="input">', '<div class="title">Input</div>', '<pre>',
               '</pre>', '</div>', '<div class="output">', '<div class="title">Output</div>',
               '<pre>', '</pre>', '</div>',
               ]


# def try_load_tests(contest_id, task_id):
#     url = 'https://codeforces.com/contest/{contest_id}/problem/{task_id}'.format(
#         contest_id=contest_id,
#         task_id=task_id
#     )
#     req = urllib.request.urlopen(url)
#     text = req.read().decode('utf-8')

#     inputs = []
#     outputs = []
#     state = 0
#     i = 0

#     while i < len(text):
#         if text[i:i + len(test_tokens[state])] == test_tokens[state]:
#             i += len(test_tokens[state])
#             state = (state + 1) % len(test_tokens)
#             if state == 3:
#                 inputs.append('')
#             if state == 8:
#                 outputs.append('')
#         else:
#             if state == 3:
#                 inputs[-1] += text[i]
#             if state == 8:
#                 outputs[-1] += text[i]
#             i += 1

#     for i in range(len(inputs)):
#         inputs[i] = inputs[i].replace('<br />', '\n').strip()

#     for i in range(len(outputs)):
#         outputs[i] = outputs[i].replace('<br />', '\n').strip()
#     if (len(inputs) != len(outputs)) or (not inputs):
#         return None, None
#     return inputs, outputs


def try_load_tests(contest_id, task_id):
    print("debug_begin 10")
    url = 'https://codeforces.com/contest/{contest_id}/problem/{task_id}'.format(
        contest_id=contest_id,
        task_id=task_id
    )
    inputs = []
    outputs = []

    useragent = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
    rqg = requests.get(url, headers=useragent, timeout=None, verify=False)
    html = rqg.content.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    data_list = soup.find_all('div', {"class": "test-example-line"})
    if len(data_list) == 0:
        data_list = soup.find_all('div', {"class": "input"})
        for data_part in data_list:
            inputs.append(data_part.text[6:])
    else:
        for data_part in data_list:
            if str(data_part)[71] == '0' or str(data_part)[70] == '0':
                inputs.append('')
            inputs[-1] += data_part.text+'\n'

    data_list = soup.find_all('div', {"class": "output"})
    for data_part in data_list:
        outputs.append(data_part.text[7:-1])

    if (len(inputs) != len(outputs)) or (not inputs):
        return None, None
    return inputs, outputs


contest_name_start = '<div style="padding: 4px 0 0 6px;font-size:1.4rem;position:relative;">'
contest_name_end = '<div style="position:absolute;right:0.25em;top:0.35em;">'


def get_contest_info(contest_id):
    url = 'https://codeforces.com/contests/' + str(contest_id)
    req = urllib.request.urlopen(url)
    text = req.read().decode()
    title = text[text.find(contest_name_start) +
                 len(contest_name_start):text.find(contest_name_end)].strip()
    return {
        'title': title
    }


def get_basename():
    return 'CodeForces'


def is_valid_url(url):
    return url.find('codeforces.com') != -1


def extract_contest_id(url):
    match = re.search(r'\d+', url)
    return match.group(0)


if __name__ == "__main__":
    inputs, outputs = try_load_tests('1741', 'C')
    print(inputs)
    print(outputs)
