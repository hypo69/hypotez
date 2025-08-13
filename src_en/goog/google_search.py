# # \file /src/goog/google_search.py
# -*- coding: utf-8 -*-

# ! .pyenv/bin/python3

""".. module:: src.goog 
	:platform: Windows, Unix
	:synopsis:"""



from lxml import html


class GoogleHtmlParser:
    """HTML Parsing class with Google Search.

    HTML pages of the Google search results and converts it into a dictionary.
    It works both with a mobile and desktop version of HTML.

    Attributes:
        Tree (html.element): a tree of a document obtained through html.fromstring ().
        user_agent (str): user agent used to get HTML Google Search."""

    def __init__(self, html_str: str, user_agent: str = 'desktop') -> None:
        """Initialization of the Parser.

        Creates a tree of a document from a string HTML.

        Args:
            HTML_STR (str): HTML Google Search in the form of a line.
            user_agent (str): user agent for HTML. It can be 'mobile' or 'desktop'.

        Returns:
            None"""
        self.tree = html.fromstring(html_str)
        if user_agent in ['mobile', 'desktop']:
            self.user_agent = user_agent
        else:
            self.user_agent = 'desktop'

    def _clean(self, content: str) -> str:
        """Cleaning the line from extra characters.

        Cleans the line of spaces and extra characters.

        Args:
            Content (str): a string for cleaning.

        Returns:
            STR: Purified line."""
        if content:
            content = content.strip()
            content = ' '.join(content.split())
            return content
        return ''

    def _normalize_dict_key(self, content: str) -> str:
        """Normalization of the line for use as a dictionary key.

        Replaces gaps for underlining, removes the colonies, leads to the lower register.

        Args:
            Content (str): line for normalization.

        Returns:
            STR: normalized line."""
        content = str(content).replace(' ', '_').replace(':', '').lower().strip('_')
        return content

    def _get_estimated_results(self) -> int:
        """Obtaining the number of search results.

        Returns the number of results found for the desktop version of Google Search.

        Returns:
            int: The number of search results."""
        estimated_results = 0
        estimated_el = self.tree.xpath('//*[@id="result-stats"]/text()')
        if len(estimated_el) > 0:
            estimated_results = int(estimated_el[0].split()[1].replace(',', ''))
        return estimated_results

    def _get_organic(self) -> list:
        """Obtaining organic search results.

        Returns a list of organic results without additional features (Snippet, Featured Snippet, etc.).

        Returns:
            List: a list of dictionaries with organic results."""
        organic = []
        for g in self.tree.xpath('//div[@class="g"]'):
            snippets = g.xpath('.//div/div/div[2]/div')
            snippet, rich_snippet = None, None
            if len(snippets) == 1:
                snippet = snippets[0].text_content()
            elif len(snippets) > 1:
                if snippets[1].xpath('.//g-review-stars'):
                    rich_snippet = snippets[1].text_content()
                    snippet = snippets[0].text_content()
                else:
                    snippet = snippets[1].text_content()
                    rich_snippet = snippets[0].text_content()

            res = {
                'url': self._clean(g.xpath('.//@href[1]')[0]),
                'title': self._clean(g.xpath('.//h3/text()')[0]),
                'snippet': self._clean(snippet),
                'rich_snippet': self._clean(rich_snippet),
            }
            organic.append(res)
        return organic

    def _get_featured_snippet(self) -> dict | None:
        """Getting FeatUred Snippet.

        If exists, returns FeatUred Snippet with the heading and URL.

        Returns:
            dict | None: a dictionary with a heading and URL or None."""
        fs = None
        snippet_el = self.tree.xpath('//div[contains(@class, "kp-blk")]')
        if snippet_el:
            snippet_el = snippet_el[0]
            heading = snippet_el.xpath('.//h3/text()')
            url = snippet_el.xpath('.//a/@href')
            if heading and url:
                fs = {'title': heading[0], 'url': url[-1]}
        return fs

    def _get_knowledge_card(self) -> dict | None:
        """Obtaining a knowledge card.

        Returns a knowledge card with a heading, a subtitle and a description, if exists.

        Returns:
            dict | NONE: Dictionary with data from knowledge card or None."""
        kc_el = self.tree.xpath('//div[contains(@class, "kp-wholepage")]')
        if kc_el:
            kc_el = kc_el[0]
            more_info = []
            for el in kc_el.xpath('.//div[contains(@data-attrid, ":/")]'):
                el_parts = el.xpath('.//span')
                if len(el_parts) == 2:
                    more_info.append({self._normalize_dict_key(el_parts[0].text_content()): el_parts[1].text_content()})
            return {
                'title': kc_el.xpath('.//h2/span')[0].text_content(),
                'subtitle': kc_el.xpath('.//div[contains(@data-attrid, "subtitle")]')[0].text_content(),
                'description': kc_el.xpath('.//div[@class="kno-rdesc"]/span')[0].text_content(),
                'more_info': more_info
            }
        return None

    def _get_scrolling_sections(self) -> list:
        """Getting data from scrolling widgets.

        Returns a list of data from widgets, for example, top stories or tweets.

        Returns:
            List: List of dictionaries with data from widgets."""
        sections = self.tree.xpath('//g-section-with-header')
        data = []
        for section in sections:
            title = section.xpath('.//h3')[0].text_content()
            section_data = []
            for data_section in section.xpath('.//g-inner-card'):
                data_title = data_section.xpath('.//div[@role="heading"]/text()')[0]
                data_url = data_section.xpath('.//a/@href')[0]
                section_data.append({'title': self._clean(data_title), 'url': self._clean(data_url)})
            data.append({'section_title': title, 'section_data': section_data})
        return data

    def get_data(self) -> dict:
        """Obtaining the final data from the search page.

        Collects data from the search results: organic results, knowledge card, etc.

        Returns:
            DICT: Dictionary with search page data."""
        data = {}
        if self.user_agent == 'desktop':
            data = {
                'estimated_results': self._get_estimated_results(),
                'featured_snippet': self._get_featured_snippet(),
                'knowledge_card': self._get_knowledge_card(),
                'organic_results': self._get_organic(),
                'scrolling_widgets': self._get_scrolling_sections()
            }
        return data
