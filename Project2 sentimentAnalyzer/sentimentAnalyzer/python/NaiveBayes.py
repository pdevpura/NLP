import sys
import getopt
import os
import math
import operator

class NaiveBayes:
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
    """NaiveBayes initialization"""
    self.FILTER_STOP_WORDS = False
    self.BOOLEAN_NB = False
    self.stopList = set(self.readFile('../data/english.stop'))
    self.numFolds = 10
    self.PosdictWordCount = {}  #Total Pos word count
    self.NegdictWordCount = {} #Total Neg words count
    self.Posdictbool = {}
    self.Posdictbool = {}
    self.PosClassCt = 0     #Pos doc count
    self.NegClassCt = 0     #Neg doc count
    self.Vocab = {}         #uniq words in all docs
    self.TotPosWords = 0    #Total number of words in pos class
    self.TotNegWords = 0    #Total number of words in neg class
    self.filcount = 0
  def find_log(self, num, denom):
      base = 2
      val=0.0
      val = math.log((float(num)/float(denom)), base)
      return val

  def word_exists(self, word,klass_l):

      if (klass_l == 'pos'):
        if (self.PosdictWordCount.has_key(word)):
            return True
        else:
            return False
      else:
        if (self.NegdictWordCount.has_key(word)):
            return True
        else:
            return False

  def word_append(self, all_word, klass_l):
      mymap = {}

      for word in all_word:

        if (klass_l == 'pos'):

            self.Vocab[word] = 1
            #self.TotPosWords += 1
            if(self.BOOLEAN_NB):

              if(not mymap.has_key(word)):
                mymap[word] =1
                self.TotPosWords += 1
                if (self.word_exists(word, klass_l)):
                  self.PosdictWordCount[word] += 1

                else:
                  self.PosdictWordCount[word] = 1
            else:
              self.TotPosWords += 1
              if (self.word_exists(word,klass_l)):
                self.PosdictWordCount[word] += 1
              else:
                self.PosdictWordCount[word] = 1
        else:
          self.Vocab[word] = 1
          #self.TotNegWords += 1
          if(self.BOOLEAN_NB):
            if (not mymap.has_key(word)):
              mymap[word] = 1
              self.TotNegWords += 1
              if (self.word_exists(word, klass_l)):
                self.NegdictWordCount[word] += 1
              else:
                self.NegdictWordCount[word] = 1
          else:
              self.TotNegWords += 1
              if (self.word_exists(word, klass_l)):
                self.NegdictWordCount[word] += 1
              else:
                self.NegdictWordCount[word] = 1


      #for word in all_word:
      #     if(self.Vocab.has_key(word)):
      #          pass
      #      else:
      #          self.Vocab[word] = 1

  def class_count(self,klass_l):
      if (klass_l=='pos'):
        self.PosClassCt += 1
      else:
        self.NegClassCt += 1

  #############################################################################
  # TODO TODO TODO TODO TODO 
  # Implement the Multinomial Naive Bayes classifier and the Naive Bayes Classifier with
  # Boolean (Binarized) features.
  # If the BOOLEAN_NB flag is true, your methods must implement Boolean (Binarized)
  # Naive Bayes (that relies on feature presence/absence) instead of the usual algorithm
  # that relies on feature counts.
  #
  #
  # If any one of the FILTER_STOP_WORDS and BOOLEAN_NB flags is on, the
  # other one is meant to be off.

  def classify(self, words):
    """ TODO
      'words' is a list of words to classify. Return 'pos' or 'neg' classification.
    """
    if self.FILTER_STOP_WORDS:
      words =  self.filterStopWords(words)
    PosProb=0.0
    NegProb=0.0
    posdenom=len(self.Vocab) + self.TotPosWords
    negdenom = len(self.Vocab) + self.TotNegWords
    for each_word in words:
      posnum = 1
      negnum = 1
      if(self.BOOLEAN_NB):
        if (self.PosdictWordCount.has_key(each_word)):
          posnum +=self.PosdictWordCount[each_word]
        if (self.NegdictWordCount.has_key(each_word)):
          #negnum +=1
          negnum +=self.NegdictWordCount[each_word]
      else:
        if(self.PosdictWordCount.has_key(each_word)):
          posnum += self.PosdictWordCount[each_word]
        if(self.NegdictWordCount.has_key(each_word)):
          negnum +=self.NegdictWordCount[each_word]



      PosProb+=self.find_log(posnum,posdenom)
      NegProb+=self.find_log(negnum,negdenom)


    PosProb += self.find_log(self.PosClassCt,self.PosClassCt+self.NegClassCt)
    NegProb += self.find_log(self.NegClassCt,self.PosClassCt+self.NegClassCt)
    #print "PosProb=", PosProb
    #print "NegProg=", NegProb
    #print "Vocab count=",len(self.Vocab)
    #print "Fil count=",self.filcount
    #print "Pos count=",self.TotPosWords
    #print "Neg count=",self.TotNegWords

    # Write code here
    if(PosProb >= NegProb):
      return 'pos'
    else:
      return 'neg'

    #return 'pos'
  

  def addExample(self, klass, words):
    """
     * TODO
     * Train your model on an example document with label klass ('pos' or 'neg') and
     * words, a list of strings.
     * You should store whatever data structures you use for your classifier 
     * in the NaiveBayes class.
     * Returns nothing
    """
    if(self.FILTER_STOP_WORDS):
        words=self.filterStopWords(words)
    self.word_append(words,klass)

    self.class_count(klass)

    #print "Pos Dict"
    #self.PosdictWordCount

    #print"Neg Dict"
    #self.NegdictWordCount


    # Write code here


      

  # END TODO (Modify code beyond here with caution)
  #############################################################################
  
  
  def readFile(self, fileName):
    """
     * Code for reading a file.  you probably don't want to modify anything here, 
     * unless you don't like the way we segment files.
    """
    contents = []
    f = open(fileName)
    for line in f:
      contents.append(line)
    f.close()
    result = self.segmentWords('\n'.join(contents)) 
    return result

  
  def segmentWords(self, s):
    """
     * Splits lines on whitespace for file reading
    """
    return s.split()

  
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

  def train(self, split):
    for example in split.train:
      words = example.words
      if self.FILTER_STOP_WORDS:
        words =  self.filterStopWords(words)
      self.addExample(example.klass, words)

#return splits and append TrainSplits for the 
  def crossValidationSplits(self, trainDir):
    """Returns a lsit of TrainSplits corresponding to the cross validation splits."""
    splits = []
    #print (trainDir)
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    #print posTrainFileNames
    #for fileName in trainFileNames:
    for fold in range(0, self.numFolds):
      split = self.TrainSplit() #split is a object of type TrainSplit
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
  
  def filterStopWords(self, words):
    """Filters stop words."""
    filtered = []
    for word in words:
      if not word in self.stopList and word.strip() != '':
        filtered.append(word)
      else:
        self.filcount += 1
    return filtered

def test10Fold(args, FILTER_STOP_WORDS, BOOLEAN_NB):
  nb = NaiveBayes()
  splits = nb.crossValidationSplits(args[0])
  avgAccuracy = 0.0
  fold = 0
  for split in splits:
    classifier = NaiveBayes()
    classifier.FILTER_STOP_WORDS = FILTER_STOP_WORDS
    classifier.BOOLEAN_NB = BOOLEAN_NB
    accuracy = 0.0
    ###Added by PD
    for example in split.train:
      words = example.words
      classifier.addExample(example.klass, words)
    
    #print classifier.PosdictWordCount,"\n"

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
    
    
def classifyDir(FILTER_STOP_WORDS, BOOLEAN_NB, trainDir, testDir):
  classifier = NaiveBayes()
  classifier.FILTER_STOP_WORDS = FILTER_STOP_WORDS
  classifier.BOOLEAN_NB = BOOLEAN_NB
  trainSplit = classifier.trainSplit(trainDir)
  classifier.train(trainSplit)
  testSplit = classifier.trainSplit(testDir)
  accuracy = 0.0
  for example in testSplit.train:
    words = example.words
    guess = classifier.classify(words)
    if example.klass == guess:
      accuracy += 1.0
  accuracy = accuracy / len(testSplit.train)
  print '[INFO]\tAccuracy: %f' % accuracy


def main():
  FILTER_STOP_WORDS = False
  BOOLEAN_NB = False
  (options, args) = getopt.getopt(sys.argv[1:], 'fbm')
  if ('-f','') in options:
    FILTER_STOP_WORDS = True
  elif ('-b','') in options:
    BOOLEAN_NB = True


  if len(args) == 2:
    classifyDir(FILTER_STOP_WORDS, BOOLEAN_NB,  args[0], args[1])
  elif len(args) == 1:
    test10Fold(args, FILTER_STOP_WORDS, BOOLEAN_NB)

if __name__ == "__main__":
  main()

