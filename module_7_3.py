import string


class WordsFinder:
    def __init__(self, *file_names):
        self.file_names = file_names

    def get_all_words(self):
        all_words = {}

        for file_name in self.file_names:
            with open(file_name, 'r', encoding='utf-8') as file:
                text = file.read().lower()
                for punct in [',', '.', '=', '!', '?', ';', ':', ' - ']:
                    text = text.replace(punct, '')

                words = text.split()

                all_words[file_name] = words

        return all_words

    def find(self, word):
        word = word.lower()
        all_words = self.get_all_words()
        result = {}

        for name, words in all_words.items():
            if word in words:
                result[name] = words.index(word) + 1

        return result

    def count(self, word):
        word = word.lower()
        all_words = self.get_all_words()
        result = {}

        for name, words in all_words.items():
            result[name] = words.count(word)

        return result


# Пример использования:
finder2 = WordsFinder('test_file.txt')

print(finder2.get_all_words())

print(finder2.find('TEXT'))

print(finder2.count('teXT'))
