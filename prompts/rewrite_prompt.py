def get_rewrite_prompt(original_title, original_content, original_url):
    """
    Génère le prompt pour la réécriture d'article par LLM.
    """
    return (
        "Rewrite the following news article so that both the title (as the first Markdown H1 heading, e.g., '# New Title') "
        "and the content are completely different from the original wording, "
        "but preserve all the information and meaning. Keep it about the same length as the original.\n\n"
        "You may add notes and definitions for technical terms in the article to enhance clarity.\n"
        "Return ONLY a valid Markdown file, starting with an H1 title, followed by the article content. "
        f"add the url of the original article at the end Url:{original_url}"
        "Do NOT include any JSON, explanations, comments, or code blocks. Only valid Markdown.\n\n"
        "Here is the original article:\n"
        f"Title: {original_title}\n"
        f"Content: {original_content}\n\n"
        "Please return your answer as a well-formatted Markdown article."
    )


__all__ = ["get_rewrite_prompt"]
