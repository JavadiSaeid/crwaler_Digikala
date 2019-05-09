import requests, getpass, codecs
from bs4 import BeautifulSoup as bs


def Digikala(username='',  password=''):
    url = "https://www.digikala.com/users/login/?_back=https%3A//www.digikala.com/"
    if (username and password) == '':
        us = input("Enter Your Username:")
        pw = getpass.getpass(prompt='Enter Your Password:')
        # password = input('Enter Your Password:')
    else:
        us = username
        pw = password
    pyload = {'login[email_phone]': us, 'login[password]': pw, 'login[remember]': 'checked'}
    session = requests.session()
    r = session.post(url, data=pyload)
    if r.status_code != 200:
        print('Can Not Connected To DigiKala.com!')
    else:
        orders = session.get("https://www.digikala.com/profile/orders/?page=1")
        soup = bs(orders.text, 'html.parser')
        titles = soup.select('title')
        title = titles[0].text
        NewUser = None
        try:
            # NewUser = soup.find('div', 'c-account-box__footer is-highlighted').span.text
            NewUserss = soup.select_one(".c-account-box__headline")
            NewUser=NewUserss.text
        except:
            pass
        if title != "Digikala" and NewUser != 'ورود به دیجی‌کالا':
            print("You Login To Digikala")
            # prettifys = soup.prettify()
            # storage = codecs.open('digi.html', 'w', 'utf-8')
            # storage.write(prettifys)
            # storage.close()
            # print("Save WebPage")

            getPages = soup.select('.js-pagination-item')
            Pages = len(getPages)
            W = 0
            if Pages == 0:
                W = 1
                Pages = 2
            AllPrice = []
            for page in range(1, Pages):
                if W != 1:
                    orders1 = session.get(f"https://www.digikala.com/profile/orders/?page={str(page)}")
                else:
                    orders1 = session.get(f"https://www.digikala.com/profile/orders")
                soup1 = bs(orders1.text,  'html.parser')
                pricess = soup1.find_all('div',  'c-table-orders__cell c-table-orders__cell--price')
                for price in pricess:
                    a = price.text
                    if a not in ['۰ ', 'مبلغ کل', 'مبلغ قابل پرداخت'] :
                        b = a.replace(' تومان',  '')
                        c = b.replace('\n', '')
                        d = c.replace(',', '')
                        e = d.replace(' ', '')
                        AllPrice.append(int(e))
            print("Total amount of your purchases: {:,} Toman From {} purchase orders".format(sum(AllPrice), len(AllPrice)))
        else:
            print("Your Username OR Password invalid!")
    input("\nEnter To Exit!")

if __name__ == "__main__" :
    Digikala()


