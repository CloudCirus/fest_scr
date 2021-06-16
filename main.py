from bs4 import BeautifulSoup
from settings import DOMAIN, URL
from fake_useragent import UserAgent
import requests
import json


headers = {'user-agent': UserAgent().opera}

decision = int(input('Do you want to save festivals links in txt file?\nInput: 1 - yes / 0 - no ...\n'))
count_1: int
count_2: int


def parser() -> None:
    """main func"""
    urls = collect_festivals_urls(urls_generator(URL))
    if decision:
        urls = save_festivals_urls_in_txt('festival_urls', urls)
    save_festivals_data_in_json('festivals', collect_festivals_data(urls))
    test(count_1, count_2)


def urls_generator(url: str) -> list:
    urls = []
    for i in range(0, 217, 24):
        generated_url = f'{url}&o={i}'
        urls.append(generated_url)
    return urls


def collect_festivals_urls(urls: list) -> list:
    festivals_urls = []
    i = 0
    for url in urls:
        response = requests.get(url, headers=headers)
        html_response = json.loads(response.text)['html']
        soup = BeautifulSoup(html_response, 'lxml')

        go_inside = soup.find_all(class_='card-details-link')
        for element in go_inside:
            festivals_urls.append(f'{DOMAIN}{element.get("href")}')
            i += 1
            print(f'collect {i} url...')
    # for test
    global count_1
    count_1 = i

    return festivals_urls


def collect_festivals_data(urls: list) -> list:
    festivals_data = []
    j = 0
    for j, url in enumerate(urls, start=1):
        response = requests.get(url, headers=headers).content
        try:
            soup = BeautifulSoup(response, 'lxml')
            go_inside = soup.find('div', class_='topcont-bgimage')
            # fest data
            fest_logo = go_inside.find('div', class_='top-image-cont').find('source').get('srcset')
            fest_info = go_inside.find('div', class_='top-info-cont')
            fest_name = fest_info.find('h1').text.strip()
            fest_date = fest_info.find('h3').text.strip()
            fest_place_name = fest_info.find('a', class_='tc-white').text
            fest_place_location = fest_info.find('a', class_='tc-white').get('href')
            fest_place_info = f'{fest_place_name} : {DOMAIN}{fest_place_location}'
            fest_age_limit = fest_info.find('a', class_='tc-white').findNext('p', class_='p-13pt').text.strip()

            tmp_data = {
                'name': fest_name,
                'logo': fest_logo,
                'date': fest_date,
                'age': fest_age_limit,
                'place': fest_place_info,
            }

            festivals_data.append(tmp_data)
            print(f'iteration {j}')
            print(f'save {fest_name.upper()} data...')

        except Exception as ex:
            print(ex)
            print('Something going wrong...')
    # for test
    global count_2
    count_2 = j

    return festivals_data


def save_festivals_urls_in_txt(file_name, festival_urls: list) -> list:
    with open(f'{file_name}.txt', 'w') as file:
        for line in festival_urls:
            file.writelines(f'{line}\n')
    with open('festival_urls.txt') as file:
        urls = [line.strip() for line in file.readlines()]
    return urls


def save_festivals_data_in_json(file_name, festival_urls: list) -> None:
    with open(f'{file_name}.json', 'a') as file:
        json.dump(festival_urls, file, indent=4, ensure_ascii=False)
        print('saving data in JSON completed')


def test(i: int, j: int) -> None:
    if i == j:
        print(f'>>>>>> ZBS!')
    else:
        print(f'>>>>>> {int(i - j)} festivals data not saved!')


if __name__ == '__main__':
    parser()
