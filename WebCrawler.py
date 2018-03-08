import re
import urllib.request as urllib2


class CommentParser:
    def __init__(self, url):
        self.url = url
        self.comment_heading = []
        self.comments = []
        self.reviews = []

    def scroll_all_the_review_page_and_find_comment(self):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]

        page_number = 1
        while True:
            previous_comments = len(self.comments)
            html_page = opener.open(self.url + '&pageNumber=' + str(page_number))
            self.calculate_amazon_review_from_review_link(html_page.read().decode('utf-8'))
            if previous_comments == len(self.comments):
                break
            page_number = page_number + 1

    def calculate_amazon_comment_product_link(self, html_page_as_string):
        regex_for_review_section = r"<div id=.*data-hook=\"review\".*>.*<\/div>"
        regex_for_review_comment_section = r"<div data-hook=\"review-collapsed\"[^>]+?>(.*?)<\/div>"
        reviews_matches = re.fianditer(regex_for_review_section, html_page_as_string)

        for matchNum, match in enumerate(reviews_matches):
            self.reviews.append(match.group())

            matched_reviews = match.group()

            comments_matches = re.finditer(regex_for_review_comment_section, matched_reviews)
            for match_comment, comment in enumerate(comments_matches):
                self.comments.append(comment)

    def calculate_amazon_review_from_review_link(self, html_page_as_string):
        # https://regex101.com/r/9SY9Ly/1
        regex_for_review_comment_section = r"<span data-hook=\"review-body\"[^>]+?>(.*?)<\/span>"

        comments_matches = re.finditer(regex_for_review_comment_section, html_page_as_string)
        for matchNum, match in enumerate(comments_matches):
            matched_review = match.group(1)
            self.comments.append(matched_review)


if __name__ == "__main__":
    parser = CommentParser('https://www.amazon.com/Canon-PowerShot-Digital-Camera-Optical/product-reviews/B00ZM1E46I/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews')
    parser.scroll_all_the_review_page_and_find_comment()

    reviews = ""
    for comment in parser.comments:
        print(comment)
        reviews += " " + comment +"\n"

xml_string_file = open('text.txt', 'w')
xml_string_file.write(reviews+ "\n")
xml_string_file.close()



