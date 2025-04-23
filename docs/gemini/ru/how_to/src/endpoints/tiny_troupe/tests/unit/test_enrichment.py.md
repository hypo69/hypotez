### Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода выполняет тестирование функциональности обогащения контента с использованием класса `TinyEnricher`. Он проверяет, что контент, сгенерированный на основе заданных требований, действительно расширен и соответствует минимальной заданной длине.

Шаги выполнения
-------------------------
1. **Определение контента для обогащения**:
   - Исходный контент (`content_to_enrich`) определяется как многострочный текст, представляющий собой стратегический документ о партнерстве WonderCode и Microsoft.

2. **Определение требований к обогащению**:
   - Устанавливаются требования (`requirements`) к процессу обогащения, указывающие на необходимость расширения исходного контента как минимум в три раза по количеству символов.

3. **Инициализация и вызов обогащения контента**:
   - Создается экземпляр класса `TinyEnricher`.
   - Вызывается метод `enrich_content` с передачей исходного контента, требований, типа контента и дополнительной контекстной информации.

4. **Проверка результата**:
   - Проверяется, что результат обогащения не равен `None`.
   - Проверяется, что длина обогащенного контента как минимум в три раза превышает длину исходного контента.

5. **Логирование**:
   - Результат обогащения, его длина и длина исходного контента логируются для отладки и анализа.

Пример использования
-------------------------

```python
import pytest
import textwrap

import logging
logger = logging.getLogger("tinytroupe")

import sys
sys.path.append('../../tinytroupe/')
sys.path.append('../../')
sys.path.append('..')

from testing_utils import *

from tinytroupe.enrichment import TinyEnricher

def test_enrich_content():

    content_to_enrich = textwrap.dedent("""
    # WonderCode & Microsoft Partnership: Integration of WonderWand with GitHub
    ## Executive Summary
    This document outlines the strategic approach and considerations for the partnership between WonderCode and Microsoft, focusing on the integration of WonderWand with GitHub. It captures the collaborative efforts and insights from various departments within WonderCode.
    ## Business Strategy
    - **Tiered Integration Approach**: Implement a tiered system offering basic features to free users and advanced functionalities for premium accounts.
    - **Market Expansion**: Leverage the integration to enhance market presence and user base.
    - **Revenue Growth**: Drive revenue through premium account conversions.
    ## Technical Considerations
    - **API Development**: Create robust APIs for seamless data exchange between WonderWand and GitHub.
    - **Security & Compliance**: Ensure user privacy and data protection, adhering to regulations.
    ## Marketing Initiatives
    - **Promotional Campaigns**: Utilize social media, tech blogs, and developer forums to promote the integration.
    - **User Testimonials**: Share success stories to illustrate benefits.
    - **Influencer Collaborations**: Engage with tech community influencers to amplify reach.
    ## Product Development
    - **Feature Complementarity**: Integrate real-time collaboration features into GitHub's code review process.
    - **User Feedback**: Gather input from current users to align product enhancements with user needs.
    ## Customer Support Scaling
    - **Support Team Expansion**: Scale support team in anticipation of increased queries.
    - **Resource Development**: Create FAQs and knowledge bases specific to the integration.
    - **Interactive Tutorials/Webinars**: Offer tutorials to help users maximize the integration's potential.
    ## Financial Planning
    - **Cost-Benefit Analysis**: Assess potential revenue against integration development and maintenance costs.
    - **Financial Projections**: Establish clear projections for ROI measurement.

    """).strip()

    requirements = textwrap.dedent("""
    Turn any draft or outline into an actual and long document, with many, many details. Include tables, lists, and other elements.
    The result **MUST** be at least 3 times larger than the original content in terms of characters - do whatever it takes to make it this long and detailed.
    """).strip()
    
    result = TinyEnricher().enrich_content(requirements=requirements, 
                                       content=content_to_enrich, 
                                       content_type="Document", 
                                       context_info="WonderCode was approached by Microsoft to for a partnership.",
                                       context_cache=None, verbose=True)    
    
    assert result is not None, "The result should not be None."

    logger.debug(f"Enrichment result: {result}\n Length: {len(result)}\n Original length: {len(content_to_enrich)}\n")

    assert len(result) >= len(content_to_enrich) * 3, "The result should be at least 3 times larger than the original content."