import os
import random
import unicodedata
import argparse
import requests
from tqdm import tqdm
from lxml import html
from lxml.etree import HTMLParser

class PublicDomainPoetryScraper:
    """ A class to scrape poems from https://www.public-domain-poetry.com/.

    """
    def __init__(self, local_path):
        """ Returns a PublicDomainPoetryScraper.

        Args:
            local_path: path where poems should be stored.

        """
        self.base_url = "https://www.public-domain-poetry.com/"
        self.local_path = local_path

    def get_authors(self) -> list[str]:
        """ Gets a list of top author pages from the site.

        """
        page = requests.get(self.base_url+"topauthors.php")
        tree = html.fromstring(page.content)
        authors = [l for l in tree.xpath('//center/table//tr//a//@href')]
        return authors
    
    def get_poems_from_author(self, author:str) -> list[str]:
        """ Gets a list of poems from an individual author.

        Args:
            author: author id string from get_authors

        """
        page = requests.get(self.base_url+author[1:])
        tree = html.fromstring(page.content)
        poems = [l for l in tree.xpath('//center/table//tr//a//@href')]
        return poems
    
    def get_poem_text_from_poem(self, poem:str) -> str:
        """ Gets the poem text for a single poem.

        Args:
            poem: poem id string from get_poems_from_author

        """
        page = requests.get(self.base_url+poem)
        parser = HTMLParser(encoding="cp1252")
        tree = html.fromstring(page.content, parser=parser)
        text = " ".join([l for l in tree.xpath('//font[@class="t3a"]//text()')])
        return text

    def get_clean_text_from_poem_text(self, text:str) -> str:
        """ Handles a few formatting rules.

        Args:
            text: text output from get_poem_text_from_poem

        """
        text = unicodedata.normalize('NFKD',text)
        text.replace("\r","")
        return text
    
    def write_text_to_local(self, author: str, poem:str, text:str) -> None:
        """ Saves poem text to a local file.

        Args:
            author: author id from get_authors
            poem: poem id from get_poems_from_author
            text: text to write.

        """
        
        if not os.path.exists(self.local_path+author[1:]):
            os.makedirs(self.local_path+author[1:])
        with open(self.local_path+poem+".txt","w", encoding='utf-8') as poem_file:
            poem_file.write(text)
    
    def load_poems(self, n_authors:int, n_poems:int, max_tokens: int):
        """ Scrapes random number of poems from popular authors and saves them.

        Args:
            n_authors: how many authors to scrape.
            n_poems: how many poems to scrape per author.
            max_tokens: only store poems under this size.

        """
        authors = self.get_authors()
        authors = random.sample(authors, n_authors)
        for author in tqdm(authors):
            poems = self.get_poems_from_author(author)
            poems = random.sample(poems, n_poems)
            for poem in tqdm(poems, position=1, leave=False):
                poem_text = self.get_poem_text_from_poem(poem)
                clean_text = self.get_clean_text_from_poem_text(poem_text)
                if len(clean_text.split(" ")) < 256:
                    self.write_text_to_local(author, poem, clean_text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--loader", help="loader type", default="public_domain_poetry")
    parser.add_argument("-a", "--authors", help="number of random authors", default=50)
    parser.add_argument("-p", "--poems", help="number of random poems", default=10)
    parser.add_argument("-m", "--max_tokens", help="max number of words per poem", default=256)
    parser.add_argument("-s", "--storage_path", help="storage path", default=".local/real/")
    args = parser.parse_args()
    if args.loader == "public_domain_poetry":
        poetry_loader = PublicDomainPoetryScraper(args.storage_path)
    else:
        raise ModuleNotFoundError("Loader %s not an option." % args.loader)
    poetry_loader.load_poems(args.authors, args.poems, args.max_tokens)