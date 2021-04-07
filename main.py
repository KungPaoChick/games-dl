import requests
import argparse
import colorama
from bs4 import BeautifulSoup as soup


class Get_Connection:
    
    def __init__(self, search_query):
        for query in search_query:
            self.query = query


    def conn(self):
        try:
            url = f"https://www.abrokegamer.com/?s={'%20'.join([x for x in self.query.split()])}"
            with requests.get(url) as response:
                response.raise_for_status()
                page_soup = soup(response.text, 'html.parser')
                
            return Get_Games(self.query, page_soup).find_game()
        except requests.HTTPError as err:
            print(colorama.Fore.RED,
                f'[!!] Something went wrong! {err}',
                colorama.Style.RESET_ALL)


class Get_Games:
    
    def __init__(self, object_query, locator):
        self.object_query = object_query
        self.locator = locator

    def find_game(self):
        print(colorama.Fore.GREEN,
            f'[*] Searching Results for: {self.object_query}', colorama.Style.RESET_ALL)

        games_data_set = {}
        for index, game in enumerate(self.locator.findAll('h2', {'class': 'title front-view-title'}), start=1):
            for game_link in game.findAll('a'):
                games_data_set[index] = {game.text : game_link['href']}
                print(f'{index} : {game.text}')
                
        while True:
            game_selection = int(input('\n\nEnter the Index of the game you want to download: '))
            if not game_selection in games_data_set:
                print(colorama.Fore.RED,
                    f'[!!] {game_selection} is an invalid selection',
                    colorama.Style.RESET_ALL)
            else:
                for element in games_data_set[game_selection]:
                    return Get_Games(self.object_query, self.locator).open_dl_page(games_data_set[game_selection][element])

    def open_dl_page(self, game_page):
        import webbrowser
        try:
            with requests.get(game_page) as game_response:
                game_response.raise_for_status()
                page_soup = soup(game_response.text, 'html.parser')

            for download_button in page_soup.findAll('a', {'rel': 'noopener noreferrer'})[:-1]:
                webbrowser.open(download_button['href'])
        except requests.HTTPError as err:
            print(colorama.Fore.RED,
                f'[!!] Something went wrong! {err}', colorama.Style.RESET_ALL)
                    
if __name__ == '__main__':
    colorama.init()
    parser = argparse.ArgumentParser(description='Downloads Cracked Games Online')

    parser.add_argument('-s', '--search',
                        nargs=1, metavar='SEARCH',
                        action='store',
                        help='Searches for games')
    
    args = parser.parse_args()
    if args.search:
        Get_Connection([x for x in args.search]).conn()
