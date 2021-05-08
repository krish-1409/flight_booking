from bs4 import BeautifulSoup,Comment
soup =    """<div class="foo">
    cat dog sheep goat
    <!--
    <p>test</p>
    -->
    </div>"""

soup = BeautifulSoup(soup)
print(soup.body.div.text)