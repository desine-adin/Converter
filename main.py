from bs4 import BeautifulSoup
from decimal import Decimal

def convert(amount, cur_from, cur_to, date, requests):
    response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp', params={"date_req":date})
    soup = BeautifulSoup(response.text, 'lxml')
    kurs_of_first = Decimal(0)
    kurs_of_second = Decimal(0)
    if cur_from == 'RUR':
        kurs_of_first = Decimal(1)
        soup_of_second_value = soup.find('charcode', text=cur_to).parent
        kurs_of_second = Decimal(soup_of_second_value.value.text.replace(',', '.')) / Decimal(
            soup_of_second_value.nominal.text)
    elif cur_to == 'RUR':
        soup_of_first_value = soup.find('charcode', text=cur_from).parent
        kurs_of_first = Decimal(soup_of_first_value.value.text.replace(',', '.')) / Decimal(
            soup_of_first_value.nominal.text)
        kurs_of_second = Decimal(1)
    else:
        soup_of_first_value = soup.find('charcode', text=cur_from).parent
        soup_of_second_value = soup.find('charcode', text=cur_to).parent
        kurs_of_first = Decimal(soup_of_first_value.value.text.replace(',', '.'))/Decimal(soup_of_first_value.nominal.text)
        kurs_of_second = Decimal(soup_of_second_value.value.text.replace(',', '.'))/Decimal(soup_of_second_value.nominal.text)
    return round(kurs_of_first/kurs_of_second*amount, 4)