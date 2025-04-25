## Как использовать этот блок кода
=========================================================================================

Описание
-------------------------
Этот блок кода проводит юнит-тестирование функции `enrich_content` из модуля `tinytroupe.enrichment`. Тест проверяет, что функция успешно обогащает исходный текст, увеличивая его размер в три раза, и что результат не является `None`.

Шаги выполнения
-------------------------
1. **Подготовка данных:** 
    - Создается тестовый текст (`content_to_enrich`) с помощью `textwrap.dedent`.
    - Создаются требования к обогащению текста (`requirements`) с помощью `textwrap.dedent`.
2. **Вызов функции:**
    - Создается экземпляр класса `TinyEnricher`.
    - Вызывается функция `enrich_content` с тестовым текстом, требованиями, типом контента, контекстной информацией и флагом `verbose`.
3. **Проверка результата:**
    - Убеждаемся, что результат не `None`.
    - Проверяем, что длина результата (`len(result)`) больше или равна длине исходного текста, умноженной на 3 (`len(content_to_enrich) * 3`).
4. **Логирование:**
    - Дебаг-сообщение с информацией о результате обогащения, длине результата и длине исходного текста.

Пример использования
-------------------------

```python
import textwrap
from tinytroupe.enrichment import TinyEnricher

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

print(result) # Вывод обогащенного текста
```