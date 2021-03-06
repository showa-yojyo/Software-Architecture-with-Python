# Code Listing #9

"""

Return top 10 most common words from the online text of the "The Hound of Baskervilles"

"""

import requests
import operator
from collections import defaultdict, Counter

print('Using defaultdict')
# requests.get(url).text でテキストを直接得る。
text = requests.get('https://www.gutenberg.org/files/2852/2852-0.txt').text
# 頻度を集計する。
freq = defaultdict(int)

for word in text.split():
    if len(word.strip()) == 0:
        continue
    freq[word.lower()] += 1

print(sorted(freq.items(),
             key=operator.itemgetter(1), reverse=True)[:10])

print('Using Counter')
# この入れ子の内包表記は覚えにくい
freq = Counter([_f for _f in [x.lower().strip() for x in text.split()] if _f])
# Counter.most_common() が急所
print(freq.most_common(10))
