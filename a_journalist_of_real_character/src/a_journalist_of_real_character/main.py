#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Run the `Journalist of Real Character` to generate an essay using a Large Language Model (LLM).

The following steps are performed:
* Load the `README.md` file of the overall repository `a_collective_essay_of_real_character`.
This provides background information about the project, and the event where expert opinions
were collected as voice transcripts.
* Load the transcripts of the different expert groups. This provides the opinions needed to
generate the essay.
* Generate the essay by using an OpenAI LLM via the corresponding API.
"""

# from openai import OpenAI
from read_parse_write import read_and_parse_sources

CONFIG = {
    "sources": [
        {
            "filepath": "../../../README.md",
            "keyword": "Methodology",
            "stop_early": 2,
        },
    ]
}


def main():
    sources = read_and_parse_sources(CONFIG)
    print(sources)

    # client = OpenAI()
    # result = client.responses.create(
    #    model="gpt-5",
    #    input="Write a haiku about code.",
    #    reasoning={"effort": "low"},
    #    text={"verbosity": "low"},
    # )
    # print(result.output_text)


if __name__ == "__main__":
    main()
