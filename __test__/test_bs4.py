from bs4 import BeautifulSoup

html = '<td class="title blink head"><div class="tit3 selected" id="t3" name="n3">' \
       '<a href="/movie/bi/mi/basic.nhn?code=136872" title="미녀와야수">미녀와야수</a></div></td>'


# 1. Tag 조회
def ex1():
    bs = BeautifulSoup(html, 'html.parser')

    tag = bs.td
    print(type(tag))
    print(tag)

    tag = bs.div
    print(tag)
    print(tag.id, tag['id'], tag.name, tag['name'])

    tag = bs.a
    print(tag)
    print(tag.name)

# 2. Attributes 값
def ex2():
    bs = BeautifulSoup(html, 'html.parser')
    tag = bs.td
    print(tag['class'])

    tag = bs.div
    print(tag.attrs)


# 3. Attributes 조회
def ex3():
    bs = BeautifulSoup(html, 'html.parser')

    tag = bs.find('td')
    print(tag)

    tag = bs.find('td', attrs={'class': 'title'})
    print(tag)

    tag = bs.find(attrs={'title': '미녀와야수'})
    print(tag)

    tag_div = bs.find(attrs={'class': 'selected'})
    tag_a = tag_div.find('a')
    print(tag_a)

if __name__ == '__main__':
    ex3()









