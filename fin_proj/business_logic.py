import os
from collections import defaultdict
from string import punctuation
from typing import List, Tuple
from config import DIR


def get_names_of_files(dir_path: str) -> dict:
    """
    Get names and path to all files in directory with extension .txt.
    Args:
        dir_path: path to the folders which will be scan
    Returns:
        defaultdict: names of file, and path to file
    """
    files_info = defaultdict(list)
    names_of_files = []
    roots_of_files = []
    for root, dirnames, filenames in os.walk(dir_path):
        for filename in filenames:
            if filename.endswith('.txt'):
                names_of_files.append(filename)
                roots_of_files.append(os.path.join(root, filename))
                files_info = {
                    "names_of_files": names_of_files,
                    "roots_of_files": roots_of_files,
                }
    return files_info


def get_count_of_files(dir_path: str) -> int:
    """
    Check number of files in directory with extension .txt.
    Args:
        dir_path: path to the folders which will be scan
    Returns: number of file
    """
    count_of_files = len(get_names_of_files(dir_path)['names_of_files'])
    return count_of_files


def preparing_files_for_word_analysis(list_of_files: list) -> list:
    """
    Preparing all files for word analysis.
    Args:
        list_of_files: list of paths to all files in base directory
    Returns: list of all words
    """
    all_words = []
    for files in list_of_files:
        with open(files, encoding="utf-8") as text:
            words = [x.strip(punctuation).lower() for x in text.read().split()]
            all_words.extend(words)
    return all_words


def get_common_and_rare_words(words: List[str]) -> dict:
    """
    Find the most common and the rarest words in list of words.
    Args:
        words: list of words
    Returns:
        dict: the most common and the rarest words in list of words
    """
    counter = defaultdict(int)
    for word in words:
        if len(word) >= 2:
            counter[word] += 1
            top_of_words = {
                "common_word": sorted(counter.items(), key=lambda item: item[1], reverse=True)[0][0],
                "rarest_word": sorted(counter.items(), key=lambda item: item[1])[0][0],
            }
    return top_of_words


def get_average_word_len(words: List[str]) -> int:
    """
    Get average length of words from list of words.
    Args:
        words: list of words
    Returns: average length of words
    """
    len_of_words = [len(word) for word in words]
    average_word_len = int(sum(len_of_words) / len(len_of_words))
    return average_word_len


def get_phonetic_analysis(words: List[str]) -> Tuple[int]:
    """
    Get number of vowels, consonants and syllables in list of words.
    Args:
        words: list of words
    Returns:
        tuple: number of vowels, consonants and syllables
    """
    VOWELS = ["a", "e", "i", "o", "u", "y", "а", "е", "ё", "и", "о", "у", "ы", "э", "ю", "я",]
    consonants = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t",
                  "v", "w", "x", "z", "б", "г", "д", "ж", "з", "й", "к", "л", "м", "н", "п", "р",
                  "с", "т", "ф", "х", "ц", "ч", "ш", "щ", "ь", "ъ",]

    count_of_vowels = 0
    count_of_consonants = 0
    for word in words:
        lowercase_word = word.lower()
        for letter in lowercase_word:
            if letter in VOWELS:
                count_of_vowels += 1
            if letter in consonants:
                count_of_consonants += 1

    syllables = count_of_vowels  # сколько в слове гласных, столько и слогов :)
    return count_of_vowels, count_of_consonants, syllables


def group_folder_info(dir_path: str) -> dict:
    """
    Group information about folder and files inside the folder into one dict.
    Args:
        dir_path: path to the folders which will be scan
    Returns:
        dict: information with characteristics of folder and files inside the folder
    """
    filenames = get_names_of_files(dir_path)["names_of_files"]
    count_of_files = get_count_of_files(dir_path)

    files_roots = get_names_of_files(dir_path)["roots_of_files"]
    prepared_words = preparing_files_for_word_analysis(files_roots)

    common_and_rare_words = get_common_and_rare_words(prepared_words)
    most_common_word = common_and_rare_words["common_word"]
    rarest_word = common_and_rare_words["rarest_word"]

    average_len_of_words = get_average_word_len(prepared_words)
    count_of_vowels = get_phonetic_analysis(prepared_words)[0]
    count_of_consonants = get_phonetic_analysis(prepared_words)[1]
    syllables = get_phonetic_analysis(prepared_words)[2]

    folder_info = {
        "count of files": count_of_files,
        "names of files": filenames,
        "the most common word": most_common_word,
        "the rarest word": rarest_word,
        "average len of words": average_len_of_words,
        "count of vowels": count_of_vowels,
        "count of consonants": count_of_consonants,
        "syllables": syllables,
    }

    return folder_info


def get_path_for_filename(name: str) -> str:
    """
    Get path to file use filename.
    Args:
        name: filename
    Returns: path to file
    """
    names_of_files = get_names_of_files(DIR)["names_of_files"]
    roots_of_files = get_names_of_files(DIR)["roots_of_files"]
    files_info = dict(zip(names_of_files, roots_of_files))
    path = files_info[name]
    return path


def group_file_info(path_to_file: str) -> dict:
    """
    Group information about file into one dict.
    Args:
        path_to_file: path to the file which will be scan

    Returns:
        dict: information with characteristics of file
    """
    all_words = []
    with open(path_to_file, encoding="utf-8") as text:
        words = [x.strip(punctuation).lower() for x in text.read().split()]
        all_words.extend(words)
        common_and_rare_words = get_common_and_rare_words(all_words)
        most_common_word = common_and_rare_words["common_word"]
        rarest_word = common_and_rare_words["rarest_word"]

        average_len_of_words = get_average_word_len(words)
        count_of_vowels = get_phonetic_analysis(words)[0]
        count_of_consonants = get_phonetic_analysis(words)[1]
        syllables = get_phonetic_analysis(words)[2]

    file_info = {
        "the most common word": most_common_word,
        "the rarest word": rarest_word,
        "average len of words": average_len_of_words,
        "count of vowels": count_of_vowels,
        "count of consonants": count_of_consonants,
        "syllables": syllables,
    }

    return file_info


def get_list_of_all_words(dir_path: str) -> list:
    """
    Get list of all words in in base directory
    Args:
        dir_path: path to the folders which will be scan

    Returns:
        list of strings: all words in all files in directory

    """
    paths_to_all_files = get_names_of_files(dir_path)["roots_of_files"]
    all_words = preparing_files_for_word_analysis(paths_to_all_files)
    return all_words


def group_word_info(word) -> dict:
    """
    Group information about word into one dict.
    Args:
        word: word

    Returns:
        dict: information with characteristics of word
    """
    len_of_word = get_average_word_len(word)
    count_of_vowels = get_phonetic_analysis(word)[0]
    count_of_consonants = get_phonetic_analysis(word)[1]
    syllables = get_phonetic_analysis(word)[2]

    word_info = {
        "len of word": len_of_word,
        "count of vowels": count_of_vowels,
        "count of consonants": count_of_consonants,
        "syllables": syllables,
    }

    return word_info
