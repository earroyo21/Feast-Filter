# from ast import increment_lineno
import requests
from bs4 import BeautifulSoup as bs
from dish import Dish


def scrape(url: str, max=-1):  # what if max entered is negative
    r = requests.get(url)
    soup = bs(r.text, 'html.parser')
    anchors = soup.findAll('a', attrs={
        'class': 'comp mntl-card-list-items mntl-document-card mntl-card card card--no-image'})

    dish_list = list()
    count = 0
    for anchor in anchors:
        dish_r = requests.get(anchor['href'])
        soup = bs(dish_r.text, 'html.parser')

        name = soup.findAll('h1')
        rating = soup.findAll('div', attrs={
            'class': 'comp type--squirrel-bold mntl-recipe-review-bar__rating mntl-text-block'})
        rating_count = soup.findAll('div', attrs={
                                    'class': 'comp type--squirrel mntl-recipe-review-bar__rating-count mntl-text-block'})
        ingredients = soup.findAll(
            'span', attrs={'data-ingredient-name': 'true'})
        ingredients_list = [ingredient.text for ingredient in ingredients]

        if rating:
            d = Dish(name[0].text, rating[0].text.rstrip().lstrip(),
                     rating_count[0].text.rstrip().lstrip(), ingredients_list)
        else:
            d = Dish(name[0].text, 'N/A', 'N/A', ingredients_list)

        dish_list.append(d)
        count += 1
        print(count)  # temporary
        if max > -1:
            if count == max:
                break
    return dish_list


urls = ['https://www.allrecipes.com/recipes/80/main-dish/',
        'https://www.allrecipes.com/recipes/17561/lunch/',
        'https://www.allrecipes.com/recipes/1214/world-cuisine/latin-american/mexican/appetizers/',
        'https://www.allrecipes.com/recipes/1217/world-cuisine/latin-american/mexican/desserts/',
        'https://www.allrecipes.com/recipes/1215/world-cuisine/latin-american/mexican/soups-and-stews/',
        'https://www.allrecipes.com/recipes/1470/world-cuisine/latin-american/mexican/authentic/',
        'https://www.allrecipes.com/recipes/732/us-recipes/amish-and-mennonite/'
        'https://www.allrecipes.com/recipes/2432/world-cuisine/latin-american/south-american/argentinian/',
        'https://www.allrecipes.com/recipes/228/world-cuisine/australian-and-new-zealander/',
        'https://www.allrecipes.com/recipes/718/world-cuisine/european/austrian/',
        'https://www.allrecipes.com/recipes/16100/world-cuisine/asian/bangladeshi/',
        'https://www.allrecipes.com/recipes/719/world-cuisine/european/belgian/',
        'https://www.allrecipes.com/recipes/1278/world-cuisine/latin-american/south-american/brazilian/',
        'https://www.allrecipes.com/recipes/1277/world-cuisine/latin-american/south-american/chilean/',
        'https://www.allrecipes.com/recipes/272/us-recipes/cajun-and-creole/',
        'https://www.allrecipes.com/recipes/733/world-cuisine/canadian/',
        'https://www.allrecipes.com/recipes/695/world-cuisine/asian/chinese/',
        'https://www.allrecipes.com/recipes/14759/world-cuisine/latin-american/south-american/colombian/',
        'https://www.allrecipes.com/recipes/709/world-cuisine/latin-american/caribbean/cuban/',
        ]
dish_list = list()
for url in urls:
    dish_list = dish_list + scrape(url, 60)
print('Recipe Count :', len(dish_list))
while True:
    print('======================')
    key = input('Enter Key Ingredient: ')
    print('======================')
    print()
    print()
    if key == 'q':
        break
    for d in dish_list:
        for ingredient in d.ingredients:
            if key in ingredient:
                print(d.name)
                print('Rating: ', d.rating, d.rating_count)
                for i in d.ingredients:
                    print('    ', end='')
                    print(i)
                break
    print()
    print()
