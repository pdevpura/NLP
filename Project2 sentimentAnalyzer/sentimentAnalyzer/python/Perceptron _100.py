import sys
import getopt
import os
import math
import operator
import random
import time
import numpy as np

class Perceptron:
  

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
    """Perceptron initialization"""
    #in case you found removing stop words helps.
    self.stopList = set(self.readFile('../data/english.stop'))
    self.numFolds = 10
    self.myset = set()
    self.w0 = []
    self.wa = []
    self.b0 = 0.0
    self.ba = 0.0
    self.ct = 1
    self.klass_dict ={'pos':1, 'neg':-1}
    self.wf = []
    self.bf = 0.0
  #############################################################################
  # TODO TODO TODO TODO TODO 
  # Implement the Perceptron classifier with
  # the best set of features you found through your experiments with Naive Bayes.

  def classify(self, words):
    """ TODO
      'words' is a list of words to classify. Return 'pos' or 'neg' classification.
    """
    word_dict = {}
    doc =[]
    calc_val =0.0

    for each_word in words:
        #if (word_dict.has_key(each_word)):
        if each_word in word_dict:
            word_dict[each_word] += 1
        else:
            word_dict[each_word] = 1

    i = 0
    for w in self.myset:
        #if (word_dict.has_key(w)):
        if w in word_dict:
            doc.append(word_dict[w])
            calc_val += float(self.w0[i]) * word_dict[w]
        else:
            doc.append(0)
        i += 1
    calc_val += self.b0
    if (calc_val >=0):
        return 'pos'
    else:
        return 'neg'

    # Write code here

    #return 'pos'
  

  def addExample(self, klass, words):
      word_dict = {}
      doc = []
      calc_val = 0.0

      klass_val = 1 if klass=='pos' else -1

      for each_word in words:
          #if(word_dict.has_key(each_word)):
          if each_word in word_dict:
              word_dict[each_word] += 1
          else:
              word_dict [each_word] = 1

      i = 0
      for w in self.myset:
          #if (word_dict.has_key(w)):
          if w in word_dict:
              temp =word_dict[w] 
              doc.append(temp)
              calc_val += float(self.w0[i])*temp
          else:
              doc.append(0)
          i += 1
      #calc_val = np.dot(self.w0,doc)
      calc_val += self.b0
      calc_val *=klass_val
      k=0
      if(calc_val <= 0):
        for ele in doc:
            self.w0[k] += ele*klass_val
            self.wa[k] += ele*klass_val*self.ct
            k +=1
            #self.w0 = [x+y*self.klass_dict[klass] for x,y,z in zip(w0,doc)]
        self.b0 += klass_val
        self.ba += klass_val*self.ct
      self.ct += 1



      """
     * TODO
     * Train your model on an example document with label klass ('pos' or 'neg') and
     * words, a list of strings.
     * You should store whatever data structures you use for your classifier 
     * in the Perceptron class.
     * Returns nothing
    """

    # Write code here

    #pass
  
  def train(self, split, iterations):
      """
      * TODO 
      * iterates through data examples
      * TODO 
      * use weight averages instead of final iteration weights
      """
      self.myset = set()
      self.w0 = []
      self.wa = []
      self.b0 = 0.0
      self.ba = 0.0
      self.ct = 1
      random.shuffle(split.train)

      for example in split.train:
          words = example.words
          self.myset.update(words)
      self.w0 = [0.0]*len(self.myset)
      self.wa = [0.0]*len(self.myset)
      start_time = time.time()
    
      for x1 in range(iterations):
        sample_ct =0
        random.shuffle(split.train)
        for example in split.train:
          words = example.words
          self.addExample(example.klass, words)
          sample_ct +=1
          if sample_ct == 200:
            break

      self.w0 = [x - float(y)/float(self.ct) for x, y in zip(self.w0, self.wa)]


      self.b0 = float(self.b0) -float(self.ba)/float(self.ct)


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


  def crossValidationSplits(self, trainDir):
    """Returns a lsit of TrainSplits corresponding to the cross validation splits."""
    splits = [] 
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    #for fileName in trainFileNames:
    for fold in range(0, self.numFolds):
      split = self.TrainSplit()
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
    return filtered

def test10Fold(args):
  pt = Perceptron()
  
  iterations = int(args[1])
  splits = pt.crossValidationSplits(args[0])
  avgAccuracy = 0.0
  fold = 0
  for split in splits:
    classifier = Perceptron()
    accuracy = 0.0
    classifier.train(split,iterations)
  
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
    
    
def classifyDir(trainDir, testDir,iter):
  classifier = Perceptron()
  trainSplit = classifier.trainSplit(trainDir)
  iterations = int(iter)
  classifier.train(trainSplit,iterations)
  testSplit = classifier.trainSplit(testDir)
  #testFile = classifier.readFile(testFilePath)
  accuracy = 0.0
  for example in testSplit.train:
    words = example.words
    guess = classifier.classify(words)
    if example.klass == guess:
      accuracy += 1.0
  accuracy = accuracy / len(testSplit.train)
  print '[INFO]\tAccuracy: %f' % accuracy
    
def main():
  (options, args) = getopt.getopt(sys.argv[1:], '')
  
  if len(args) == 3:
    classifyDir(args[0], args[1], args[2])
  elif len(args) == 2:
    test10Fold(args)

if __name__ == "__main__":
    main()
