import argparse
import os
from bs4 import BeautifulSoup
import requests
import validators
import logging
import re
import json
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

class SimpleScraper():
    def __init__(self, url, output="results.json", tag ="", pattern="*", show_matches=True, src=False):
        self.url = url
        self.output = os.path.join(output)
        self.pattern = pattern
        self.with_src = src
        self.tag = tag
        self.show_matches = show_matches
    def url_validity_check(self, url):
        return validators.url(url)
    
        
    def get_html(self, url):
        if self.url_validity_check(url):
            try:
                response = requests.get(url)
                logger.debug("Url successfully reached")
                return response.text
            except Exception as e:
                logger.error(f"Fatal: the web page can't be reached. Details: {e}")
                exit()
        else:
            logger.error("Fatal: the URL isn't valid")
            exit()
        
    def scrap(self, html):
        try:
            soup = BeautifulSoup(html, "html.parser")
            regex = re.compile(self.pattern)
            logger.debug(f'Launching find_all with the tag "{self.tag}", the pattern "{self.pattern}" and src on "{self.with_src}"')
            
            if self.with_src:
                matches = soup.find_all(self.tag, src=True, recursive=True)
            else:
                matches = soup.find_all(self.tag, string=regex, recursive=True)
            
            logger.info(f"Matched with {matches} elements")
            
            if self.show_matches:
                if len(matches) > 20:
                    answer = self.ask_to_user(f"There is {len(matches)}. Do you really want to show it?(y/n) ")
                    if answer:
                        logging.info("MATCHED WITH:")
                        for element in matches:
                            logger.info(element)
            
            return matches
        except Exception as e:
            logger.error(f"Fatal: The web page's code can't be extracted. Details: {e}")
            exit()
    
    def ask_to_user(self, ask, print_if_yes=None, print_if_no=None):
        while True:
                user_review = input(ask)
                if user_review.lower() == "y":
                    return True
                elif user_review.lower() == "n":
                    logger.info()
                    return False
                else:
                    logger.error("Please enter a valid input: y to validate, n to cancel")
                    
    def writes_results(self, matches, html):
        if os.path.isdir(self.output) or os.path.isfile(self.output):
            answer = self.ask_to_user(
                f"{self.output} already exists. Overwrite?(y/n) ",
                print_if_no="Operation canceled, exiting..."
            )
            if not answer:
                exit()
        
        with open(self.output, "w") as r:
            json.dump({"matches": matches, "html": html}, r)
        logger.info(f"Output is available at {self.output}")
        
    def run(self):
        html = self.get_html(self.url)
        matches = self.scrap(html)
        self.writes_results(matches, html)
        
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser("Simple Scraper")
    
    parser.add_argument("url", help="The url you want to scrap. Like https://exemple.com")
    parser.add_argument("--extract-tag", "-t", default=None, help="A tag to extract. Must be without brackets. Can be combined with --find")
    parser.add_argument("--only-src", "-os", action="store_true", help="To get only tag with an src link. This args cancels --find, but doesn't cancel --extract-tag")
    parser.add_argument("--find", "-f", default=".*", help="Specific pattern to find. Exemple: --find \"<button>\". Support regex like \"<*>\". Can be combined with --extract-tag") #We give by default a regex which match with everythings. We can also use "string=True" with bs4 to match with everythings
    parser.add_argument("--output", "-o", default="results.json", help="The path, relative or absolute, where you want to save the results")
    parser.add_argument("--show-matches", "-s", action="store_true", help="To shows the results before writing it")
    parser.add_argument("--debug", action="store_true", help="Shows debug logs")
    
    args = parser.parse_args()
    
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    simple_scraper = SimpleScraper(args.url, output=args.output, tag=args.extract_tag, pattern=args.find, show_matches=args.show_matches, src=args.only_src)
    
    simple_scraper.run()