import os
import random
import argparse
import re
from tqdm import tqdm
import openai

class OpenAIPoetryGenerator:
    """ A class to use the OpenAI GPT-3 API to write novel poems.

    """
    def __init__(self, local_path:str, real_path:str):
        """ Returns a OpenAIPoetryGenerator.

        Args:
            local_path: path where poems should be stored.
            real_path: path where real poems are stored.

        """
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.local_path = local_path
        self.real_path = real_path

    def get_poem_title(self, author: str) -> str:
        """ Generates a novel poem title using examples from real_path.

        Args:
            author: directory containing real poem examples.

        """
        titles = os.listdir(self.real_path+author)
        titles = [" ".join(title.split("-")[:-1]) for title in titles]
        title_list = "\n".join([title.capitalize() for title in titles])
        response = openai.Completion.create(
            engine="davinci",
            prompt="Below is a list of poem titles.\n\n"+title_list,
            temperature=0.7,
            max_tokens=16,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        title_lines = response['choices'][0]['text'].split("\n")
        for ix in range(len(title_lines)):
            if title_lines[ix] != '':
                return title_lines[ix]
        ''
    
    def get_poem_content(self, author: str, poet: str, poem_title: str, max_tokens:int) -> str:
        """ Generates a novel poem using a fake title and real poet.

        Args:
            author: directory containing real poem examples.
            poet: a poet name as a string.
            poem_title: a fake poem title to generate.
            max_tokens: maximum number of tokens to generate for poems.

        """
        poems = os.listdir(self.real_path+author)
        random_poem = random.sample(poems,1)[0]
        with open(self.real_path+author+"/"+random_poem, "r", encoding="utf-8") as example_file:
            example_poem = example_file.read()
        example_title = " ".join(t.capitalize() for t in random_poem.split("-")[:-1])
        response = openai.Completion.create(
            engine="davinci",
            prompt="Below are several poems by %s.\n1. %s\n%s\n\n2. %s"%(poet, example_title, example_poem, poem_title),
            temperature=0.7,
            max_tokens=max_tokens,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop="3."
        )
        return response['choices'][0]['text']
    
    def get_poem_from_poet_real_path(self, author: str, max_tokens:int):
        """ Generates a novel poem using real_path.

        Args:
            author: directory containing real poem examples.
            max_tokens: maximum number of tokens to generate for poems.

        """
        author_name = author[:-1]
        poet = " ".join(poet_name.capitalize() for poet_name in author_name.split("-"))
        title = self.get_poem_title(author)
        if title != '' and title is not None:
            self.write_text_to_local(author,
                                     re.sub('[^\w\-_\. ]', '', title.lower().replace(" ","-")),
                                     self.get_poem_content(author, poet, title, max_tokens))
    
    def write_text_to_local(self, author: str, poem:str, text:str) -> None:
        """ Saves poem text to a local file.

        Args:
            author: author id from get_authors
            poem: poem id from get_poems_from_author
            text: text to write.

        """
        
        if not os.path.exists(self.local_path+author):
            os.makedirs(self.local_path+author)
        with open(self.local_path+author+"/"+poem+".txt","w", encoding='utf-8') as poem_file:
            poem_file.write(text)

    def generate_poems(self, n_authors: int, n_poems: int, max_tokens: int):
        """ Generates and saves n_poems poems for each of n_authors authors.

        Args:
            n_authors: number of random authors to generate poems for.
            n_poems: number of random poems to generate per author.
            max_tokens: maximum number of tokens to generate for poems.

        """
        author_dirs = os.listdir(self.real_path)
        authors = random.sample(author_dirs, n_authors)
        for author in tqdm(authors):
            for _ in tqdm(range(n_poems), position=1, leave=False):
                self.get_poem_from_poet_real_path(author, max_tokens)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--generator", help="generator type", default="open_ai")
    parser.add_argument("-a", "--authors", help="number of random authors", default=1)
    parser.add_argument("-p", "--poems", help="number of new poems", default=1)
    parser.add_argument("-m", "--max_tokens", help="max number of words per poem", default=300)
    parser.add_argument("-r", "--real_path", help="real storage path", default=".local/real/")
    parser.add_argument("-o", "--output_path", help="output storage path", default=".local/fake/")
    args = parser.parse_args()
    if args.generator == "open_ai":
        poetry_generator = OpenAIPoetryGenerator(args.output_path, args.real_path)
    else:
        raise ModuleNotFoundError("Generatr %s not an option." % args.generator)
    poetry_generator.generate_poems(int(args.authors), int(args.poems), int(args.max_tokens))
