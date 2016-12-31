import time
import sys
import getopt
import os
import math
import operator
import copy
from sets import Set
import re


class Turney:
    class TrainSplit:
        """Represents a set of training/testing data. self.train is a list of Examples, as is self.test.
            """

        def __init__(self):
            self.train = []
            self.test = []

    class Example:
        """Represents a document with a label. klass is 'pos' or 'neg' by convention.
           words is a list of strings.
        """

        def __init__(self):
            self.klass = ''
            self.words = []

    def __init__(self):
        """Turney initialization"""
        self.numFolds = 10
        self.Posdict = {}  # Total Pos word count
        self.Negdict = {}  # Total Neg words count
        self.poor_hits=0
        self.exe_hits=0
        #Pattern as described in the paper
        self.list1 = [['JJ'], ['RB', 'RBR', 'RBS'], ['JJ'], ['NN', 'NNS'], ['RB', 'RBR', 'RBS']]
        self.list2 = [['NN', 'NNS'], ['JJ'], ['JJ'], ['JJ'], ['VB', 'VBD', 'VBN', 'VBG']]
        self.list3 = [[], ['NN', 'NNS'], ['NN', 'NNS'], ['NN', 'NNS'], []]
    #function that computes the log
    def find_log(self, num, denom):
        base = 2
        val = 0.0
        val = math.log((float(num) / float(denom)), base)
        return val
    # classify the document as positive or negative
    def classify(self, word_list):
        """ TODO
          'words' is a list of words to classify. Return 'pos' or 'neg' classification.
        """

        word_list_len = len(word_list)
        so_val = 0.0
        #search for all the words in the test document that have phrases present in dictionary
        for i in range(word_list_len - 1):
            num = 1.0
            denom = 1.0
            each_word = word_list[i]
            split_word = each_word.split("_")
            found = 0
            split_word[0]=split_word[0].lower()
            # print split_word[1]
            for k in range(len(self.list1)):
                is_pos=0
                is_neg=0
                if split_word[1] in self.list1[k]:
                    split_word2 = word_list[i + 1].split("_")
                    split_word2[0]=split_word2[0].lower()
                    for m in range(len(self.list2)):
                        if split_word2[1] in self.list2[m]:
                            if (i == word_list_len - 2) or (m == 0) or (m == 4):
                                if (split_word[0], split_word2[0]) not in self.Posdict:

                                    num = 0.01*self.poor_hits
                                    is_pos=1
                                else:
                                    num = self.Posdict[(split_word[0],split_word2[0])]*self.poor_hits
                                if (split_word[0], split_word2[0]) not in self.Negdict:
                                    is_neg = 1
                                    denom = 0.01*self.exe_hits

                                    #print split_word[0], split_word2[0]
                                else:
                                    denom = self.Negdict[(split_word[0],split_word2[0])]*self.exe_hits
                                found = 1
                                so_val+=self.find_log(num,denom)


                                break
                                # print split_word[0], split_word2[0]

                            else:
                                split_word3 = word_list[i + 2].split("_")
                                if (split_word3[1] != 'NNS') and (split_word3[1] != 'NN'):
                                    if (split_word[0], split_word2[0]) not in self.Posdict:
                                        # dict[(split_word[0], split_word2[0])] = 1
                                        num = 0.01 * self.poor_hits
                                        is_pos=1
                                        #print split_word[0], split_word2[0]

                                    else:
                                        num = self.Posdict[(split_word[0], split_word2[0])] * self.poor_hits
                                    if (split_word[0], split_word2[0]) not in self.Negdict:
                                        # dict[(split_word[0], split_word2[0])] = 1
                                        denom = 0.01 * self.exe_hits
                                        is_neg=1
                                        #print split_word[0], split_word2[0]
                                    else:
                                        denom = self.Negdict[(split_word[0], split_word2[0])] * self.exe_hits
                                    if not (is_pos and is_neg):
                                        so_val += self.find_log(num, denom)
                                    #print so_val
                                    found =1
                                    break

                    #if found == 1:
                       #break
        #print so_val
        if so_val >= 0:
            return 'pos'
        else:
            return 'neg'
    #identify the execellent and poor phrase and find the surrounding the words.
    def identify_phrase(self,data,word,word_list1,word_list2):
        data_len = len(data)
        #print word,data
        split_word=[]
        indices=[]
        for i,x in enumerate(data):
            split_word=x.split('_')
            split_word[0]=split_word[0].lower()
            if split_word[0]==word:
                indices.append(i)
                #print "indices: ",indices
        #indices = [i for i, x in enumerate(data) if x == word]

        if len(indices)>0:
            #print 'Found'
            for index in indices:
                if index <= 10 and data_len - index <= 10:
                    word_list1 = data[:index]
                    word_list2 = data[index:]
                elif index <= 10 and data_len - index >= 10:
                    word_list1 = data[:index]
                    word_list2 = data[index:index + 11]
                elif index >= 10 and data_len - index <= 10:
                    word_list1 = data[index - 10:index]
                    word_list2 = data[index:]
                else:
                    word_list1 = data[index - 10:index]
                    word_list2 = data[index:index + 11]
                if word == 'excellent':
                    self.exe_hits +=1
                elif word == 'poor':
                    self.poor_hits += 1
                else:
                    print "DO nOT COME HERE"

                self.fill_dict(word_list1, word)
                self.fill_dict(word_list2, word)

    #Fill the dictionary corresponding to execllent and poor phrases
    def fill_dict(self,word_list,word):
        # word_list = line.split()
        if word == 'excellent':
            dict=self.Posdict
        elif word == 'poor':
            dict=self.Negdict
        else:
            print "DO NOT COME HERE"
        word_list_len = len(word_list)
        for i in range(word_list_len - 1):
            each_word = word_list[i]
            split_word = each_word.split("_")
            split_word[0]=split_word[0].lower()
            found = 0
            # print split_word[1]
            for k in range(len(self.list1)):

                if split_word[1] in self.list1[k]:
                    split_word2 = word_list[i + 1].split("_")
                    split_word2[0]=split_word2[0].lower()
                    for m in range(len(self.list2)):
                        if split_word2[1] in self.list2[m]:
                            if (i == word_list_len - 2) or (m == 0) or (m == 4):
                                if (split_word[0], split_word2[0]) not in dict:
                                    dict[(split_word[0], split_word2[0])] = 1
                                    #print split_word[0], split_word2[0]
                                else:
                                    dict[(split_word[0], split_word2[0])] += 1
                                    #print "never"
                                found = 1
                                break
                                # print split_word[0], split_word2[0]

                            else:
                                split_word3 = word_list[i + 2].split("_")
                                if (split_word3[1] != 'NNS') and (split_word3[1] != 'NN'):
                                    if (split_word[0], split_word2[0]) not in dict:
                                        dict[(split_word[0], split_word2[0])] = 1
                                    else:
                                        dict[(split_word[0], split_word2[0])] += 1
                                        #print "never"
                                    found = 1
                                    break

                    if found == 1:
                        break

    def addExample(self, klass, words):
        """
         * TODO
         * Train your model on an example document with label klass ('pos' or 'neg') and
         * words, a list of strings.
         * You should store whatever data structures you use for your classifier
         * in the Turney class.
         * Returns nothing
        """
        word_list1=''
        word_list2=''

        if klass =='pos':
            self.identify_phrase(words,'excellent',word_list1,word_list2)
            #print "here"
            #self.fill_dict(word_list1,self.Posdict)
            #self.fill_dict(word_list2,self.Posdict)
        elif klass =='neg':
            self.identify_phrase(words, 'poor', word_list1, word_list2)
            #self.fill_dict(word_list1, self.Negdict)
            #self.fill_dict(word_list2, self.Negdict)
        else:
           print "DO NOT ENTER"

    def readFile(self, fileName):
        """
         * Code for reading a file.  you probably don't want to modify anything here,
         * unless you don't like the way we segment files.
        """
        with open(fileName, 'r') as myfile:
            data = myfile.read().replace('\n', ' ')
        new_data=[]
        for p in data.split():
            c= p.split('_')
            if(p[0]==','or p[0]=='.' or p[0]==')' or p[0]=='(' or p[0] ==':' or p[0] == ';' or p[0]=='"' or p[0]=="``" or p[0]=='?' or p[0]=="''" or p[0]=='""' or p[0]=='!'):
                continue
            else:
                new_data.append(p)
                '''
        	data = data.replace(',', '')
        data = data.replace('.', '')
        data = data.replace(')','')
        data = data.replace('(','')
        data = data.replace(':','')
        data =data.replace(';','')
        data =data.replace('"','')
        #data2=data.split()
        #data3 = [x.lower() for x in data2]
        #print data3

        return data.split()
        '''
        return new_data


    def trainSplit(self, trainDir):
        """Takes in a trainDir, returns one TrainSplit with train set."""
        split = self.TrainSplit()
        posTrainFileNames = os.listdir('%s/pos/' % trainDir)
        negTrainFileNames = os.listdir('%s/neg/' % trainDir)
        for fileName in posTrainFileNames:
            example = self.Example()
            example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
            example.klass = 'pos'
            split.train.append(example)
        for fileName in negTrainFileNames:
            example = self.Example()
            example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
            example.klass = 'neg'
            split.train.append(example)
        return split

    def crossValidationSplits(self, trainDir):
        """Returns a lsit of TrainSplits corresponding to the cross validation splits."""
        splits = []
        #print (trainDir)
        posTrainFileNames = os.listdir('%s/pos/' % trainDir)
        negTrainFileNames = os.listdir('%s/neg/' % trainDir)
        # print posTrainFileNames
        # for fileName in trainFileNames:
        for fold in range(0, self.numFolds):
            split = self.TrainSplit()  # split is a object of type TrainSplit
            for fileName in posTrainFileNames:
                example = self.Example()
                example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
                example.klass = 'pos'
                if fileName[2] == str(fold):
                    split.test.append(example)
                else:
                    split.train.append(example)
            for fileName in negTrainFileNames:
                example = self.Example()
                example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
                example.klass = 'neg'
                if fileName[2] == str(fold):
                    split.test.append(example)
                else:
                    split.train.append(example)
            splits.append(split)
        return splits




def test10Fold(args):
    nb = Turney()
    splits = nb.crossValidationSplits(args)
    avgAccuracy = 0.0
    fold = 0
    for split in splits:
        classifier = Turney()
        accuracy = 0.0
        ###Added by PD
        for example in split.train:
            words = example.words
            classifier.addExample(example.klass, words)
        #print "POS",classifier.Posdict
        #print "NEG",classifier.Negdict
        # print classifier.PosdictWordCount,"\n"
        #print 'done'

        for example in split.test:
            words = example.words
            guess = classifier.classify(words)
            if example.klass == guess:
                accuracy += 1.0

        accuracy = accuracy / len(split.test)
        avgAccuracy += accuracy
        print '[INFO]\tFold %d Accuracy: %f' % (fold, accuracy)
        fold += 1
    avgAccuracy = avgAccuracy / fold
    print '[INFO]\tAccuracy: %f' % avgAccuracy


def main():
    args = ''
    if len(sys.argv) == 2:
        args = sys.argv[1]
    else:
        print "Give correct arguments"
    print args
    test10Fold(args)

if __name__ == "__main__":
    main()
