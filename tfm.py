from pprint import pprint
import re
import numpy as np
import PyPDF4
import os

DOCUMENTS_PATH = 'documents'

terms = ['film',
         'kin',
         'nagr',
         'produk',
         'aktor',
         'histori',
         'obraz',
         'warstw',
         'adapt',
         'gatun']


def run():
    directory = os.listdir(DOCUMENTS_PATH)
    file_paths = load_files(directory)
    articles = read_files(file_paths)
    print(articles.keys())
    counts = {}
    counts_vectors = []
    header = "Article                    |\t"

    for k, v in articles.items():
        if v is None:
            continue
        text = ''.join(v).split()
        counts[k] = {}
        for term in terms:
            counts[k][term] = 0
            for word in text:
                if word.lower().find(term) > -1:
                    counts[k][term] += 1
    for k in counts.keys():
        print("{}: {}".format(k, counts[k]))

    rows = []
    for term in terms:
        while len(term) < 20:
            term = term + " "
        header = header + "{} |\t".format(term)
    header = header + "\n"
    rows.append(header)
    index = 0
    for k in articles.keys():
        vector = []
        columns = ""
        columns = columns + "D{}".format(index)
        index += 1
        while len(columns) < 27:
            columns = columns + " "
        columns = columns + "|\t"
        for term in terms:
            num = (str(counts[k][term]))
            vector.append(int(counts[k][term]))
            while len(num) < 20:
                num = num + " "
            columns = columns + "{} |\t".format(num)
        columns = columns + "\n"
        rows.append(columns)
        counts_vectors.append(vector)
    vector_info = []
    index = 0
    for vector in counts_vectors:
        vector_info.append({'vector': vector,
                            'length': calc_vector_length(vector),
                            'index': index})
        index = index+1

    vector_distances = []
    for vector in vector_info:
        current = vector['vector']
        row = []
        for other_vector in vector_info:
            other = other_vector['vector']
            distance = round(calc_distance_between_vectors(current, other)/(vector['length'] * other_vector['length']),
                             5)
            row.append(distance)
        vector_distances.append(row)
    pprint(vector_distances)
    #print("".join(rows))


def read_files(file_paths):
    articles = {}
    for path in file_paths:
        articles[path.split("/")[-1].split(".")[0]] = read_file(path)
    return articles


def read_file(path):
    pages = []
    try:
        with open(path, 'rb') as article:
            file = PyPDF4.PdfFileReader(article)
            for i in range(file.numPages):
                page = file.getPage(i)
                pages.append(re.sub('\W+', ' ', page.extractText()))
        return pages
    except:
        print("Error with {}".format(path))


def load_files(directory):
    file_paths = []
    for file in directory:
        filename = os.fsdecode(file)
        if filename.endswith('.pdf'):
            file_paths.append(DOCUMENTS_PATH+"/"+os.path.relpath(file))
    return file_paths


def calc_vector_length(vector: list):
    added = 0
    for num in vector:
        added += num**2
    return added**(1/2)


def calc_distance_between_vectors(vector1: list, vector2: list):
    if len(vector1) != len(vector2):
        raise ArithmeticError()
    sum = 0
    for i in range(len(vector1)):
        sum += vector1[i] * vector2[i]
    return sum


if __name__ == "__main__":
    run()

