import json

def assemble_prompt(prompt_skeleton_str, methodology_sources, transcript_sources):
    """
    Assemble the prompt for the Journalist.

    Args:
        prompt_skeleton_str: The skeleton prompt as a string.
        methodology_sources: List of dictionaries containing
        parsed information from the methodology sources.
        transcript_sources: List of parsed transcript sources,
        where each source is a string (encoded in Markdown).
    
    Returns:
        prompt_str: The prompt for the Journalist as a string.
    """
    methodology_str = json.dumps(methodology_sources)
    transcript_str = sum(transcript_sources)
    prompt_str = prompt_skeleton_str.format(
        methodology_str = methodology_str,
        transcript_str = transcript_str,
    )
    return prompt_str

