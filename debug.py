import sys
sys.path.insert(0, r'C:\Users\André Elias\ceasa_forecast\src')
from bs4 import BeautifulSoup

main_page_html = '''
<html>
<body>
    <div class="generic">
        <h2>FRUTAS</h2>
        <a href="/frutas/detail">Saiba Mais</a>
    </div>
</body>
</html>
'''
soup = BeautifulSoup(main_page_html, "html.parser")
print('Soup:', soup)
frutas_heading = soup.find(string="FRUTAS")
print('frutas_heading:', frutas_heading)
print('type:', type(frutas_heading))
if frutas_heading:
    parent = frutas_heading.find_parent(class_="generic")
    print('parent:', parent)
    if parent:
        link = parent.find("a", string="Saiba Mais")
        print('link:', link)
        if link:
            print('href:', link.get("href"))