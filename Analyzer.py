import re
import csv
import nltk
import pymorphy2

from nltk.corpus import stopwords

morph = pymorphy2.MorphAnalyzer()
nltk.download('russian')


def get_normal_form(word):
    return morph.parse(word)[0].normal_form


class Analyzer(object):
    def __init__(self, text, filename):
        self.text = text
        self.filename = filename
        self.words_dict = {}
        self.words_array = []
        self.stop_words = set(stopwords.words("russian"))
        self.text_accumulator = ''
        self.start_analysis()

    def start_analysis(self):
        self.start_filtration()
        self.reformat_to_array()
        self.start_merge_sort()
        self.convert_csv()

    def start_filtration(self):
        self.text_accumulator = re.sub(r'((Статья|Глава|Раздел|КонсультантПлюс:) .{0,}\n.{0,}|([(].{0,}[)])|,|[.]|:|;|-|[0-9])', '', self.text)
        self.text_accumulator = nltk.word_tokenize(self.text_accumulator)

        for word in self.text_accumulator:
            word_normal = get_normal_form(word)
            if word_normal not in self.stop_words:
                self.words_dict[word_normal] = self.words_dict.get(word_normal, 0) + 1

    def reformat_to_array(self):
        for item in self.words_dict.items():
            self.words_array.append({'word': item[0], 'count': item[1]})

    def start_merge_sort(self):
        def merge(left_list, right_list):
            sorted_list = []
            left_list_index = right_list_index = 0

            left_list_length, right_list_length = len(left_list), len(right_list)

            for _ in range(left_list_length + right_list_length):
                if left_list_index < left_list_length and right_list_index < right_list_length:

                    if left_list[left_list_index]['count'] >= right_list[right_list_index]['count']:
                        sorted_list.append(left_list[left_list_index])
                        left_list_index += 1

                    else:
                        sorted_list.append(right_list[right_list_index])
                        right_list_index += 1

                elif left_list_index == left_list_length:
                    sorted_list.append(right_list[right_list_index])
                    right_list_index += 1

                elif right_list_index == right_list_length:
                    sorted_list.append(left_list[left_list_index])
                    left_list_index += 1

            return sorted_list

        def merge_sort(nums):
            if len(nums) <= 1:
                return nums

            mid = len(nums) // 2
            left_list = merge_sort(nums[:mid])
            right_list = merge_sort(nums[mid:])

            return merge(left_list, right_list)

        self.words_array = merge_sort(self.words_array)

    def convert_csv(self):
        file = open(f"{self.filename}.csv", 'w')
        with file:
            writer = csv.writer(file)
            for word in self.words_array:
                writer.writerow([word['word'], word['count']])