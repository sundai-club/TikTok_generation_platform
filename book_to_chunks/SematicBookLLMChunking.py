from dotenv import load_dotenv
from langchain.text_splitter import TextSplitter
from typing import List, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import re
import tiktoken

load_dotenv()


# AAH fuck this.. too much engineering for a hack.. maybe later if EPUb sin't enough..
class LLMTextSplitter(TextSplitter):
    """
    Splitting text using a large language model (like GPT-4), with options for different types of topic splitting.
    """
    def __init__(
            self,
            model_name: str = "gpt-3.5-turbo",
            prompt_type: str = "wide",
            count_tokens: bool = False,
            encoding_name: str = "cl100k_base",
            **kwargs: Any
    ) -> None:
        """
        Initialize the LLM splitter with a model chain, a prompt type, and an optional token counter.
        """
        super().__init__(**kwargs)
        self.model_name = model_name
        self.count_tokens = count_tokens
        self.encoding_name = encoding_name
        self.model = ChatOpenAI(model=self.model_name)
        self.output_parser = StrOutputParser()

        splitting_topic_template = """Split the text according to the broad topics it deals with and add >>> and <<< around each chunk: {text}"""

        self.prompt_tempalte = ChatPromptTemplate.from_template(splitting_topic_template)

        self.chain = self.prompt_tempalte | self.model | self.output_parser

    def num_tokens_from_string(self, string: str) -> int:
        """
        Count the number of tokens in a string based on a specified encoding.
        """
        encoding = tiktoken.get_encoding(self.encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def split_text(self, text: str) -> List[str]:
        """
        Split incoming text and return chunks using the model chain.
        Optionally counts the tokens if enabled.
        """
        if self.count_tokens:
            token_count = self.num_tokens_from_string(text)
            print(f"Token count of input text: {token_count}")

        response = self.chain.invoke({"text": text})
        return self._format_chunks(response)
