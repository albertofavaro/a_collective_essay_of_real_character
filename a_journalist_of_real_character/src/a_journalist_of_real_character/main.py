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

from openai import OpenAI
from read_parse_write import read_and_parse_methodology_sources
from read_parse_write import read_and_parse_transcript_sources
from engineer_prompt import assemble_prompt

# Inputs are kept here for users to customise the Journalist.
CONFIG = {
    "methodology_sources": [
        {
            "filepath": "../../../README.md",
            "keyword": "Methodology",
            "stop_early": 2,
        },
        {
            "filepath": "../../../question_sheet/group_1_2.md",
            "keyword": "Instructions",
            "stop_early": 1,
        },
        {
            "filepath": "../../../leader_summary/leader_summary.md",
            "keyword": "Methodology",
            "stop_early": None,
        },
    ],
    "transcript_sources_directory_path": "../../../transcript",
    "prompt_skeleton_filepath": "../../prompt_skeleton/prompt_skeleton.md",
    "model": "gpt-5-2025-08-07",
    "reasoning": {"effort": "medium"},
    "temperature": 1,
    "text": {"verbosity": "medium"},
}


def main():
    # Read in, and parse all sources.
    methodology_sources = read_and_parse_methodology_sources(CONFIG)
    transcript_sources = read_and_parse_transcript_sources(
        CONFIG["transcript_sources_directory_path"]
    )

    # Read in the prompt skeleton.
    with open(CONFIG["prompt_skeleton_filepath"], "r") as f:
        prompt_skeleton_str = f.read()

    # Assemble the prompt.
    prompt_str = assemble_prompt(
        prompt_skeleton_str, methodology_sources, transcript_sources
    )

    # Call the LLM.
    client = OpenAI()
    print("Calling OpenAI, please hold.")
    result = client.responses.create(
        model=CONFIG["model"],
        input=prompt_str,
        reasoning=CONFIG["reasoning"],
        temperature=CONFIG["temperature"],
        text=CONFIG["text"],
    )
    print(result.output_text)


if __name__ == "__main__":
    main()
