import requests
from bs4 import BeautifulSoup
import pandas as pd


def fix_bads(page):
    """
    Prepares html for parsing
    :param page: raw data
    :return: fixed html
    """
    page = page.replace("&amp;#34;", '"')
    page = page.replace("&amp;lt;", "<")
    page = page.replace("&amp;gt;", ">")
    page = page.replace("&gt;", ">")
    page = page.replace("&lt;", "<")
    page = page.replace("&#34;", '"')
    return page


def convert_string(text):
    """
    Converts string from ascii to utf
    :param text:
    :return:
    """
    text = text.replace("&amp;", '')
    text = text.replace("amp;", '')
    text = text.replace(";", '')
    splt = text.split(sep=" ")
    out_t = ""
    for entry in splt:
        entry_f = entry.replace(',', '')
        entry_f = entry_f.replace('(', '')
        entry_f = entry_f.replace(')', '')
        w_splt = entry_f.split(sep="#")
        out_t += convert_to_utf(w_splt[1:]) + " "
        if w_splt[0] != '':
            out_t += w_splt[0] + " "
    return out_t


def convert_to_utf(word):
    """
    Converts word to utf
    :param word:
    :return:
    """
    w = ""
    for a in word:
        w += chr(int(a))
    return w


def get_problem(page):
    """
    Get question
    :param page: prepared html page
    :return:
    """
    soup = BeautifulSoup(page, "html.parser")
    convert = soup.find_all(class_="problem")
    out_data = []
    for i, entry in enumerate(convert):
        pr_txt = entry.find_all(class_="response-fieldset-legend")
        answers = entry.find_all(class_="response-label field-label label-inline")
        answers_c = entry.find_all(class_="response-label field-label label-inline choicegroup_correct")
        out_data.append({'id': i,
                         'problem': convert_string(pr_txt[0].get_text()),
                         'answers': process_answers(answers + answers_c)})
    return out_data


def process_answers(answers):
    """
    Finds correct answers
    :param answers:
    :return:
    """
    answer_arr = []
    for answer in answers:
        inp = answer.find_all("input")
        try:
            if inp[0]['checked'] == 'true':
                if "&amp;" in answer.get_text():
                    answer_arr.append(answer.get_text().split(sep="&amp;")[0].replace("&#39", '"'))
        except KeyError:
            pass
    # Да, это костыль. Ну и что?
    while len(answer_arr) < 4:
        answer_arr.append("—")
    return answer_arr


def authorizer(username, password, URL='https://sso.openedu.ru/login/', next_page='/oauth2/authorize%3Fstate%3DYpbWrm0u6VoE6nOvTi47PQLaC5CB5ZFJ%26redirect_uri%3Dhttps%3A//openedu.ru/complete/npoedsso/%26response_type%3Dcode%26client_id%3D808f52636759e3616f1a%26auth_entry%3Dlogin'):
    """
    Authorizes and return request.session
    :param username: uname
    :param password: pwd
    :param URL: login url
    :param next_page: redirect url
    :return: request.session with all tokens
    """
    client = requests.session()
    csrf = client.get(URL).cookies['csrftoken']
    login_data = dict(username=username, password=password, csrfmiddlewaretoken=csrf, next=next_page)
    r = client.post(URL, data=login_data, headers=dict(Referer=URL))
    return client


def save_to_excel(data, filename="out.xlsx"):
    """
    Saving data to excel
    :param data: JSON from get_problem
    :param filename: name of excel file
    :return:
    """
    df = pd.DataFrame(columns=['question', 'answer1', 'answer2', 'answer3', 'answer4'])
    for rec in data:
        df = df.append({'question': rec['problem'],
                        'answer1': rec['answers'][0],
                        'answer2': rec['answers'][1],
                        'answer3': rec['answers'][2],
                        'answer4': rec['answers'][3]}, ignore_index=True)
    df.to_excel(filename)
