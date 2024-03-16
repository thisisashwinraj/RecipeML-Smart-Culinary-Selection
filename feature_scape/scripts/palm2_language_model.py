# Author: Ashwin Raj <thisisashwinraj@gmail.com>
# License: GNU Affero General Public License v3.0
# Discussions-to: github.com/thisisashwinraj/RecipeML-Recipe-Recommendation

# Copyright (C) 2023 Ashwin Raj

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""
This module provides a Python interface for utilizing the PaLM Language Model for 
text generation. The module include the class, that allows users to interact with 
PaLM API for generating textual content & another for paraphrasing generated text.

Depending on individual cases, the program may be modified to use multiprocessing 
capailities to increase the speed of data processing, on eligible local computers.
The usage of each class & their methods are described in corresponding docstrings.

Classes and Functions:
    [1] PaLMLanguageModel (class)
        [a] generate_text

    [2] PaLMPromptModule (class)
        [a] generate_recipe_preperation_time_prompt

.. versionadded:: 1.3.0
.. versionupdated:: 1.3.0

Learn about RecipeML :ref:`RecipeML: Recipe recommendation using Google PaLM APIs`
"""
import re
import ast
import pprint
import google.generativeai as palm


class PaLMLanguageModel:
    """
    Wrapper class for interacting with Google PaLM, for recipe details generation

    This class encapsulates the functionality to generate text using the PaLM API.
    It provides a convenient interface for initializing the API key, & generating
    text based on a given prompt. The API key is maintained as a streamlit secret.

    Class Methods:
        [1] generate_text

    .. versionadded:: 1.3.0
    .. versionupdated:: 1.3.0

    The performance of the methods present in the class can be optimized by using
    the CPUPool via the multithreading capailities on eligible local/cloud system.
    """

    def __init__(self, api_key):
        """
        Initialize PaLMLanguageModel with the PaLM API key, and configure the API

        Parameters:
            [str] api_key: API key required to authenticate & access the PaLM API
        """
        self.api_key = api_key
        palm.configure(api_key=self.api_key)

    def generate_text(self, prompt, randomness=0.7, max_response_length=1000):
        """
        Method to generate recipe description using Google Pathway Language model

        This method utilizes PaLM's text generation capabilities to generate text
        output, based on given prompt. Generated text output is influenced by the
        specified randomnes level & is constrained by the maximum response length.

        Read more in the :ref:`RecipeML:DataWrangling & Fundamental PreProcessing`

        .. versionadded:: 1.3.0

        Parameters:
            [str] prompt: The input prompt to guide the recipe generation process
            [float] randomness: The level of randomness in recipe text generation
            [int] max_response_length: Maximum output token of the generated text

        Returns:
            [str] padded_start_string: Generated recipe based on the given prompt
        """
        completion = palm.generate_text(
            model="models/text-bison-001",
            prompt=prompt,
            temperature=randomness,
            max_output_tokens=max_response_length,
        )

        return completion.result  # Returns description generated by the PaLM API


class PaLMPromptModule:
    """
    Class for generating the prompt tailored for PaLM API-based recipe generation.

    This class provides methods to generate prompts for the PaLM API specifically
    designed for calculating preparation time. These are universal across the app.

    Class Methods:
        [1] generate_recipe_preperation_time_prompt

    .. versionadded:: 1.3.0

    The performance of the methods present in the class can be optimized by using
    the CPUPool via the multithreading capailities on eligible local/cloud system.
    """

    def __init__(self):
        pass

    def generate_recipe_preperation_time_prompt(self, recipe_name):
        """
        Method to generate the recipe preperation time, & the serving size prompt

        Read more in the :ref:`RecipeML:DataWrangling & Fundamental PreProcessing`

        .. versionadded:: 1.3.0

        Parameters:
            [str] recipe_name: Name of cuisine, for which the prompt is generated

        Returns:
            [str] prompt: PaLM API prompt for generating prep time & serving size
        """
        prompt = f"""
        You are an expert chef with extensive knowledge of preparing a wide variety of recipes.
        Calculate the usual preperation time for preparing the recipe named {recipe_name}, the accurate number of calories in it, and the type of this cuisine (like continental, chinese, indian etc).
        Return a python list of length 3 with the preperation time (in minutes), calorie count (integer value), and the type of cuisine.
        Do not add headings. Keep the list minimalist.
        """
        return prompt
