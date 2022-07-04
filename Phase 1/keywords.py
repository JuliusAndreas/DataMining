from rake_nltk import Rake

with open('dataset.txt') as f:
    contents = f.read()

r = Rake()
r.extract_keywords_from_text(contents)

for rating, keyword in r.get_ranked_phrases_with_scores():
    if rating > 9:
        print(rating, keyword)