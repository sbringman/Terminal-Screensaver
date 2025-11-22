import random as rand
import re
import logging
import wikipediaapi

def print_title(title: str, term_width: int) -> None:
    """ Prints the title of the Wikipedia article at the top of the terminal

    Parameters
    ----------
    title : str
        The title of the article
    
    term_width : int
        The width of the terminal
    """

    title_len = len(title)

    first_line = " +" + "-"*(title_len+2) + "+"
    first_line += " "*(term_width - len(first_line))

    second_line = " | " + title + " |"
    second_line += " "*(term_width - len(second_line))

    third_line = first_line

    print()
    print(first_line)
    print(second_line)
    print(third_line)
    print()

    return

def format_summary(summary: str, term_width: int) -> str:
    """ Formats the Wikipedia summary by placing line breaks in the correct places

    Parameters
    ----------
    summary : str
        The summary text to be formatted
    
    term_width : int
        The width of the terminal
    
    Returns
    -------
    summary : str
        The formatted summary
    """
    

    line_length = 0
    right_edge_gap = 2
    length = len(summary)

    # Start by doubling line breaks
    summary = summary.replace("\n", "\n\n")

    # Need to tack on an extra space so it knows where the end of the
    # summary is
    summary += " "


    for i in range(length):
        if summary[i] == "\n":
            line_length = 0
        elif summary[i] != " ":
            pass
        elif summary[i] == " ":
            # If there is not another space between here and the end of the line,
            # then substitute this space with a newline
            if " " not in summary[i+1: i+(term_width - right_edge_gap - line_length)+1] and \
                "\n" not in summary[i+1: i+(term_width - right_edge_gap - line_length)+1]:
                summary = summary[:i] + "\n" + summary[i+1:]
                line_length = 0
        
        line_length += 1

    summary = summary.replace("\n\n\n", "\n\n")

    return summary


def clean_links(links: list) -> list:
    """ Removes links that don't go to Wikipedia articles 
    from the list of links. Removes links that go to templates or categories.

    Parameters
    ----------
    links : list
        The list of links to Wikipedia articles
    
    Returns
    -------
    links : list
        The cleaned list
    """

    cleaned_links = []

    # Clean link list
    for link in links.keys():
        if "Template:" in link:
            break
        elif "Template " in link:
            break
        elif "Category:" in link:
            break

        else:
            cleaned_links.append(link)

    return cleaned_links


def choose_page(wiki: wikipediaapi.Wikipedia, cur_title: str, logger: logging.Logger) -> wikipediaapi.WikipediaPage:
    """ Chooses the next Wikipedia page for the random walk

    Parameters
    ----------
    wiki : wikipediaapi.Wikipedia
        The Wikipedia object
    
    cur_title : str
        The title of the current Wikipedia article
    
    logger : logging.Logger
        The logger to keep track of the visited pages
    
    Returns
    -------
    page : wikipediaapi.WikipediaPage
        The next Wikipedia page
    """
    
    cur_page = wiki.page(cur_title)

    # If the current page doesn't exist, go back to
    # the unusual articles page
    if not cur_page.exists():
        logger.info(f"The page {cur_title} doesn't exist. Restarting...")
        cur_page = wiki.page('Wikipedia:Unusual articles')
        logger.info(f"{cur_page.title}")

    links = cur_page.links
    cleaned_links = clean_links(links)

    # If there are no valid links, go back to the unusual
    # articles page
    if len(cleaned_links) == 0:
        logger.info("Found no links, restarting...")
        cur_page = wiki.page('Wikipedia:Unusual articles')
        logger.info(f"{cur_page.title}")
        links = cur_page.links
        cleaned_links = clean_links(links)

    new_link = rand.choice(cleaned_links)
    page = wiki.page(f'{new_link}')

    max_iter = 5

    # Try to find a valid link
    while not page.exists() and max_iter > 0:
        new_link = rand.choice(cleaned_links)
        page = wiki.page(f'{new_link}')
        max_iter -= 1

    # If a valid link was found, return the page
    if page.exists():
        return page

    # If no valid links were found, go back to the unusual
    # articles page
    logger.info("Found no links, restarting...")
    cur_page = wiki.page('Wikipedia:Unusual articles')
    logger.info(f"{cur_page.title}")

    links = cur_page.links
    cleaned_links = clean_links(links)
    new_link = rand.choice(cleaned_links)
    page = wiki.page(f'{new_link}')
    logger.info(f"{page.title}")

    return page


def display_prev_walk():
    """ Displays the list of article titles from the previous random walk
    """

    # Gets the log file for the previous walk
    with open("./logs/article_path.log") as log_file:
        logs = log_file.readlines()
    
    # Remove the date line
    logs = logs[1:]

    # This is the pattern of the log file
    log_pattern = r'INFO:root:(.*)$'

    # Prints out the titles
    print()
    for log in logs:
        if re.match(log_pattern, log):
            print(re.match(log_pattern, log).group(1))
    
    print()

    return