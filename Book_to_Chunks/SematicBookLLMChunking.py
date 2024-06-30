from dotenv import load_dotenv
from langchain.text_splitter import TextSplitter
from typing import List, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import re
import tiktoken

load_dotenv()


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

    # Define two types of prompt templates
    wide_topic_template = """Split the text according to the broad topics it deals with and add >>> and <<< around each chunk: {text}"""
    granular_topic_template = """Split the text into detailed, granular topics and add >>> and <<< around each chunk: {text}"""
