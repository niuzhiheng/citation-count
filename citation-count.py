
# coding: utf-8

import fnmatch
import os
import re
from string import rstrip
import argparse
import string

def find_authors(bib_file):
    fp = open(bib_file, "rt")
    lines = fp.read().replace('\n','')
    fp.close()
    pattern = '\s*author\s*=\s*{([^{}]*)}'
    prog = re.compile(pattern)
    lines = re.findall(pattern,lines.lower())
    return map(lambda x:x.split(' and '),lines)

def rough_same_author(name_src,name_dst):
    pattern = re.compile('[^,\w]+')
    name_src = pattern.sub('', name_src).split(',')
    name_dst = pattern.sub('', name_dst).split(',')
    if name_src[0]   !=name_dst[0]   : return False
    if name_src[1][0]!=name_dst[1][0]: return False
    return True

def is_author_included(author,authors):
    for person in authors:
        if rough_same_author(author,person):
            return True
    return False

def is_any_included(authors_src,authors_dst):
    for author in authors_src:
        if is_author_included(author,authors_dst):
            return True
    return False

def count_citation(author_list,coauthors,spot_author):
    self_cite = 0;
    coauthor_cite = 0;
    other_cite = 0;
    for authors in author_list:
        if is_author_included(spot_author,authors):
            self_cite += 1
        elif is_any_included(coauthors,authors):
            coauthor_cite += 1
        else:
            other_cite += 1
    return self_cite,coauthor_cite,other_cite

def run(base_file,spot_id,cite_file):
    author_list = find_authors(cite_file)
    coauthors = find_authors(base_file)[0]
    spot_author = coauthors.pop(spot_id)
    print 'spot_author: ',spot_author
    print 'coauthors: ',coauthors
    self_cite,coauthor_cite,other_cite = count_citation(author_list,coauthors,spot_author)
    print "self_cite: ", self_cite
    print "coauthor_cite: ", coauthor_cite
    print "other_cite: ", other_cite
    print "total_cite: ", len(author_list)

#run('base.bib',1,'science.bib')


parser = argparse.ArgumentParser(description='Citation Counting Tool -- NIU ZHIHENG')
parser.add_argument('-b', action='store', dest='base_file',
        type=str, default='base.bib',
        help='Bibtex file containing the base paper we are counting for. (only one record)')
parser.add_argument('-c', action='store', dest='cite_file',
        type=str, default='cite.bib',
        help='Bibtex file containing all the citations to the base paper. (many records)')
parser.add_argument('-i', action='store', dest='spot_id',
        type=int,default=0,
        help='The index to spot the author whom is considered for self_cite. Others are coauthors.')

if __name__ == '__main__':
    opts = parser.parse_args()
    run(opts.base_file,opts.spot_id,opts.cite_file)

