import requests
import re
import csv
from bs4 import BeautifulSoup

is_header = False
article_num = 1
idx = 0

while article_num < 1037277:
    try:

        url = f"https://sportowefakty.wp.pl/kategoria/{article_num}"
        article = requests.get(url)
        soup = BeautifulSoup(article.content, "html.parser")

        # Author
        author = soup.find(
            "strong", class_="indicator__authorname").text.strip().lower()
        # print(author)

        # Category
        ol = soup.find("ol", typeof="BreadcrumbList")
        span = ol.find_all("a")[1]
        category = span.find("span", property="name").text.strip().lower()
        # print(category)

        # About
        about = soup.find("span", class_="h3").text.lower()
        # print(about)

        # Date Time
        date = soup.find("time")
        date_string = date.get("datetime")
        # print(date_string)
        date_pattern = re.compile(r"(\d{4})-(\d{2})-(\d{2}) (\d{2})")
        date_result = date_pattern.findall(date_string)
        # print(date_result)

        year = date_result[0][0]
        month = date_result[0][1]
        day = date_result[0][2]
        hour = date_result[0][3]

        # Comments Count
        comments = soup.find("span", class_="comment_h1")
        comments_count = comments.get("data-stage")
        print(comments_count)

        # Article Snippet
        snippet = soup.find(class_="article").find_all("p")[0].text
        # print(snippet)

        # Writing to a file

        with open('sf_scrape.csv', 'a', newline='', encoding="utf-8") as csvfile:
            if is_header == False:
                fieldnames = ['ID', 'Author', 'Category',
                              "About", "Year", "Month", "Day", "Hour", "Comments", "Snippet"]
                header_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                header_writer.writeheader()
                is_header = True

            row_data = [idx, author, category, about,
                        year, month, day, hour, comments_count, snippet]
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(row_data)

        print(f"Scraped article #{article_num}")
        idx += 1
        article_num += 1

    except AttributeError:
        print(f"Artykuł {article_num} nie istnieje lub został usunięty")
        article_num += 1
        continue
