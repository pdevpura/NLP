import sys
import getopt
import os
import math
import operator

class viterbi:
    def __init__(self):
        self.prob_list = {}
        self.prob_dict = {}
        self.sent =[]
        self.dp_tab = {}
        self.forward_dp_tab = {}
        self.bp_dict = {}
        self.def_val = 0.0001
        self.tag_list = ('noun','verb','prep','inf')
        self.res= []
        self.best_seq_prob = 0.0
        self.new_order = ['noun','verb','inf','prep']
        self.orig_sent=[]
    def initialize(self):
        self.dp_tab={}
        self.forward_dp_tab={}
        self.bp_dict={}
        self.best_seq_prob=0.0
        self.res = []
    def parse_prob_file(self,probs_file):
        f = open(probs_file)
        for line in f:
            sp_line = line.split()
            sp_line =[lower_line.lower() for lower_line in sp_line]
            if(sp_line[0]) not in self.prob_dict:
                self.prob_dict[sp_line[0]]={}
            self.prob_dict[sp_line[0]][sp_line[1]] = float(sp_line[2])
            #self.prob_list[(sp_line[0],sp_line[1])] = float(sp_line[2])
        #self.print_dict()
        #print self.prob_dict
    def print_dict(self):
        for k in self.prob_list:
            print k,"  ",self.prob_list[k]

    def parse_sent_file(self,sent_file):
        f = open(sent_file)
        for line in f:
            self.orig_sent.append(line)
            self.sent.append(line.lower())
        #print self.sent[0]
        #self.viterbi_dp_prob()

    def display_sentence(self,one_sent,orig_sent):

        print "\nPROCESSING SENTENCE: ",orig_sent
        #print "\n"
        print "FINAL VITERBI NETWORK"
        #sent = one_sent.split()

        sent = orig_sent.split()
        ct = 1
        while (ct<=len(sent)):
            #for each_tag in self.dp_tab[ct]:
            for each_tag in self.new_order:

                #'{0:.16f}'.format(1.6)
                prob = '{0:.10f}'.format(self.dp_tab[ct][each_tag])
                #print "P(",sent[ct-1],"=",each_tag,")=",self.dp_tab[ct][each_tag]
                print "P(", sent[ct - 1], "=", each_tag, ")=", prob

            ct += 1
        #Final Backptr display

        print "\nFINAL BACKPTR"
        ct = 2
        while(ct<=len(sent)):
            #for each_tag in self.bp_dict[ct]:
            for each_tag in self.new_order:
                #prob = '{0:.10f}'.format(self.bp_dict[ct][each_tag])
                print "Backptr(",sent[ct-1],"=",each_tag,")=",self.bp_dict[ct][each_tag]
                #print "Backptr(", sent[ct - 1], "=", each_tag, ")=", prob
            ct+=1

        #Best Sequence Tag has probability
        #print "\nBEST TAG SEQUENCE HAS PROBABILITY = ",self.best_seq_prob
        print "\nBEST TAG SEQUENCE HAS PROBABILITY = ", '{0:.10f}'.format(self.best_seq_prob)

        ct = len(sent) - 1
        for k2 in self.res:
            print sent[ct],"->",k2
            ct -= 1

        #FOrward DP Table display
        ct = 1
        print "\nFORWARD ALGORITHM RESULTS"
        while (ct <= len(sent)):
            #for each_tag in self.forward_dp_tab[ct]:
            for each_tag in self.new_order:
                prob = '{0:.10f}'.format(self.forward_dp_tab[ct][each_tag])
                #print "P(", sent[ct - 1], "=", each_tag, ")=", self.forward_dp_tab[ct][each_tag]
                print "P(", sent[ct - 1], "=", each_tag, ")=", prob

            ct += 1





    def viterbi_dp_prob(self,k):
        each_sent = self.sent[k]
        #for one_sent in self.sent:
        #one_sent = self.sent[0].split()
        one_sent = each_sent.split()
        #print one_sent
        sent = " ".join(one_sent)
        #sent = 'bears fish'
        #one_sent = ('bears','fish')
        self.dp_tab[0]={}
        self.dp_tab[0]['phi'] = 1
        self.forward_dp_tab[0]={}
        self.forward_dp_tab[0]['phi']= 1
        ct = 1
        #print one_sent
        for each_word in one_sent:
            self.dp_tab[ct]={}
            self.forward_dp_tab[ct]={}
            self.bp_dict[ct] ={}
            #print "each_word ", each_word
            for each_tag in self.tag_list:
            #for each_tag in self.prob_dict[each_word]:
                #print "TAG ",each_tag
                val = 0.0
                max_val = 0.0
                self.forward_dp_tab[ct][each_tag] = 0.0
                if each_word in self.prob_dict:
                    if each_tag in self.prob_dict[each_word]:
                        val_each_tag = self.prob_dict[each_word][each_tag]
                        #print "val = ", val_each_tag
                    else:
                        val_each_tag = 0.0001
                else:
                    val_each_tag = 0.0001

                for prev_tag in self.dp_tab[ct-1]:
                    #print "prev_tag",prev_tag
                    if prev_tag in self.prob_dict[each_tag]:
                        prev_tag_val = self.prob_dict[each_tag][prev_tag]
                    else:
                        #print "NOT FOUND",each_tag," ",prev_tag
                        prev_tag_val = 0.0001
                    val = self.dp_tab[ct-1][prev_tag] * prev_tag_val * val_each_tag
                    val2 = self.forward_dp_tab[ct-1][prev_tag]*prev_tag_val*val_each_tag
                    self.forward_dp_tab[ct][each_tag]+=val2
                    #self.dp_tab[ct][each_tag] = self.dp_tab[ct-1][prev_tag] * self.prob_dict[each_tag][prev_tag] * val_each_tag
                    if (max_val < val):
                        self.bp_dict[ct][each_tag] = prev_tag
                        self.dp_tab[ct][each_tag] = val;
                        max_val = val
            ct += 1
        val =0.0
        max_val = 0.0
        each_tag = 'fin'
        for prev_tag in self.dp_tab[ct-1]:
            if prev_tag in self.prob_dict[each_tag]:
                prev_tag_val = self.prob_dict[each_tag][prev_tag]
            else:
                prev_tag_val = 0.0001

            val = self.dp_tab[ct - 1][prev_tag] * prev_tag_val
            # self.dp_tab[ct][each_tag] = self.dp_tab[ct-1][prev_tag] * self.prob_dict[each_tag][prev_tag] * val_each_tag
            if (max_val < val):
                #self.bp_dict[ct][each_tag] = prev_tag
                #self.dp_tab[ct][each_tag] = val;
                tag_so_far = prev_tag
                max_val = val
        #print "last tag", tag_so_far
        #self.best_seq_prob = self.dp_tab[len(one_sent)][tag_so_far]
        self.best_seq_prob = max_val
        self.res.append(tag_so_far)
        #print self.bp_dict
        ct -= 1
        while (ct> 1):
            #print self.bp_dict[ct][tag_so_far]
            tag_so_far = self.bp_dict[ct][tag_so_far]
            self.res.append(tag_so_far)
            ct -= 1
        self.display_sentence(sent,self.orig_sent[k])
def main():
    print sys.argv
    args = sys.argv[1:]
    if len(args)>2 or len(args)<2:
        print "Please give correct inputs"
    prob_file = args[0]
    sent_file = args[1]
    vb = viterbi()
    vb.parse_prob_file(prob_file)
    vb.parse_sent_file(sent_file)
    k = 0
    for k in range(len(vb.sent)):
        vb.viterbi_dp_prob(k)
        vb.initialize()
        print "\n"
    #print vb.prob_dict
    #print vb.dp_tab
    #print vb.res
    #print vb.bp_dict






if __name__ == "__main__":
  main()
