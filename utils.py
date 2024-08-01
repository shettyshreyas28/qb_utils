import re
from bs4 import BeautifulSoup

def initial_cleanup(html_string):
    html_string = re.sub(r' \\/>', '>', html_string)
    html_string = html_string.replace('&#39;', '\'')
    html_string = html_string.replace('\\"', '"').replace('\\\\', '\\')
    html_string = html_string.replace('\\,', ',')
    html_string = html_string.replace('\\/', '/')
    html_string = html_string.replace('<\\/', '</')
    html_string = html_string.replace('\u00a0', ' ')
    html_string = html_string.replace('\\u00a0\\', ' \\')
    html_string = html_string.replace('&nbsp;', ' ')
    html_string = html_string.replace('&ndash;', '-')
    html_string = html_string.replace('&amp;', '&')
    html_string = html_string.replace('\n', ' ')
    return html_string

def get_clean_text(html_string):
    html_string = initial_cleanup(html_string)

    soup = BeautifulSoup(html_string, 'html.parser')
    divs = soup.find_all('div')

    text = []
    for div in divs:
        for element in div.contents:
            if element.name is None:
                text.append(element.text)
            elif element.name == 'img':
                text.append(element.get('alt', ''))
            elif element.name == 'sub':
                text.append('_' + '{' + element.text.strip() + '}')
            elif element.name == 'sup':
                text.append('^' + '{' + element.text.strip() + '}')
            else:
                text.append(element.text)
    return ''.join(text).strip()

def get_clean(html_string):
    html_string = initial_cleanup(html_string)
    index = html_string.find('<div')
    if index == 0 or index == 1:
        return get_clean_text(html_string)
    else:
        html_string = '<div>' + html_string + '</div>'
    return get_clean_text(html_string)

def clean_options(x):
    x = eval(x)
    if x == []:
        return ''
    else:
        options = []
        for opt in x:
            options.append(get_clean(opt))
        return ', '.join(options)
