import os
import openai

class OpenAIPoetryGenerator:
    """ A class to use the OpenAI GPT-3 API to write novel poems.

    """
    def __init__(self, local_path:str):
        """ Returns a OpenAIPoetryGenerator.

        Args:
            local_path: path where poems should be stored.

        """
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.local_path = local_path

    def get_poem_title(self, poet_real_path: str) -> str:
        """ Generates a novel poem title using examples from real_path.

        Args:
            poet_real_path: directory containing real poem examples.

        """
        titles = os.listdir(poet_real_path)
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
    
    def get_poem_content(self, poet: str, poem_title: str) -> str:
        """ Generates a novel poem using a fake title and real poet.

        Args:
            poet: a poet name as a string.
            poem_title: a fake poem title to generate.

        """
        response = openai.Completion.create(
            engine="davinci",
            prompt="Below is a poem written by %s.\n%s"%(poet, poem_title),
            temperature=0.7,
            max_tokens=512,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return response['choices'][0]['text']
    
    def get_poem_from_poet_real_path(self, poet_real_path: str) -> tuple[str,str]:
        """ Generates a novel poem using real_path.

        Args:
            poet_real_path: directory containing real poem examples.

        """
        author = poet_real_path.split("/")[-2]
        poet = " ".join(poet_name.capitalize() for poet_name in author.split("-"))
        title = self.get_poem_title(poet_real_path)
        if title != '':
            self.write_text_to_local(author+"/", title.lower().replace(" ","-"), self.get_poem_content(poet, title))
    
    def write_text_to_local(self, author: str, poem:str, text:str) -> None:
        """ Saves poem text to a local file.

        Args:
            author: author id from get_authors
            poem: poem id from get_poems_from_author
            text: text to write.

        """
        
        if not os.path.exists(self.local_path+author):
            os.makedirs(self.local_path+author)
        with open(self.local_path+author+poem+".txt","w", encoding='utf-8') as poem_file:
            poem_file.write(text)

