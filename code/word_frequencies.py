# -*- coding: utf-8 -*-
import nltk
import codecs
import re
import numpy as np
import cPickle as pickle

DATA_DIR = "../data/"
DATA_DIR2 = "/srv/data/fnewspapers/"

n_words = 0

def get_tokens(filenames):
    global n_words
    for fn in filenames:
        f = codecs.open(DATA_DIR2 + "nlf_rawtext_fin/" + fn, 'r', 'utf8')
        text = f.read()
        text = text.lower()
        text = re.sub(u'[^a-zåäö ]', '', text)
        f.close()
        #tokens = nltk.tokenize.word_tokenize(text)
        tokens = text.split()
        n_words += len(tokens)
        for token in tokens:
            if len(token) > 3:
                yield token

def get_common_words(filenames, n=10000):
    """
    Get n most frequent words from given files and their occurrences.
    """
    tokens = get_tokens(filenames)
    fdist = nltk.FreqDist(tokens)
    return fdist.most_common(n)

def socialist_issns():
    sis = []
    f = open(DATA_DIR + "socialist_papers.csv", 'r')
    for line in f:
        parts = line.split(';')
        sis.append(parts[2])
    return sis

def get_filenames(wanted_issn=None, max_n=1000):
    print "Reading newspaper files..."
    fname = DATA_DIR2 + 'nlf_newspapers_fin.csv'
    names = []
    with open(fname, 'r') as f:
        i = 0
        for line in f:
            if i == 0:
                i += 1
                continue
            parts = line.split(',')
            name = parts[0]
            issn = parts[1]
            if wanted_issn is None or issn == wanted_issn:
                names.append(name)
            i += 1
    print "%d matching files in total." % len(names)
    print "Read."
    if len(names) > max_n:
        return names[:max_n]
    else:
        return names

def identify_keywords(freqs):
    print "Loading baseline frequencies..."
    (bl_freqs, bl_total) = pickle.load(open("/srv/work/unigrams.pckl", "rb"))
    print "Loaded."
    res = []
    for (word, count) in freqs:
        frac = float(count) / n_words
        if word not in bl_freqs:
            continue
        bl_frac = float(bl_freqs[word]) / bl_total
        #diff = frac - bl_frac
        diff = frac / bl_frac
        res.append((diff, word, frac, bl_frac))
    res = sorted(res, key=lambda tup: tup[0])
    return res

if __name__ == "__main__":
    #print socialist_issns()
    files = get_filenames(wanted_issn="fk14802")
    print files[:5]
    freqs = get_common_words(files)
    kws = identify_keywords(freqs)
    for res in kws:
        print "%s\t%f\t%f\t%f" % (res[1], res[0], res[2], res[3])
    #for (i,fr) in enumerate(freqs):
    #    print (u"%d\t%d\t%s" % (i+1, fr[1], fr[0])).encode('utf-8')