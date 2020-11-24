import json

with open("../data/research_papers/complete_dataset/ms_JOCCH_filled_aff.json", "r", encoding="utf-8") as f:
    articles = json.load(f)
    with open("../data/research_papers/no_country_dataset/ms_JOCCH.json", "r", encoding="utf-8") as fd:
        articles_no_abs = json.load(fd)
        for article1 in articles:
            if article1 is not None:
                for article2 in articles_no_abs:
                    if article2 is not None:
                        if article2["abstract"] is None and article1["abstract"] is not None:
                            article2["abstract"] = article1["abstract"]

with open("../data/research_papers/no_country_dataset/ms_JOCCH.json", "w", encoding="utf-8") as fu:
    json.dump(articles_no_abs, fu, ensure_ascii=False)