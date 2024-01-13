# Copyright 2020-2022 Paul Lu
import sys
import copy     # for deepcopy()

Debug = False   # Sometimes, print for debugging.  Overridable on command line.
InputFilename = "file.input.txt"
TargetWords = [
        'outside', 'today', 'weather', 'raining', 'nice', 'rain', 'snow',
        'day', 'winter', 'cold', 'warm', 'snowing', 'out', 'hope', 'boots',
        'sunny', 'windy', 'coming', 'perfect', 'need', 'sun', 'on', 'was',
        '-40', 'jackets', 'wish', 'fog', 'pretty', 'summer'
        ]

# Student write:
Stop_Words = [
    "i", "me", "my", "myself", "we", "our",
    "ours", "ourselves", "you", "your",
    "yours", "yourself", "yourselves", "he",
    "him", "his", "himself", "she", "her",
    "hers", "herself", "it", "its", "itself",
    "they", "them", "their", "theirs",
    "themselves", "what", "which", "who",
    "whom", "this", "that", "these", "those",
    "am", "is", "are", "was", "were", "be",
    "been", "being", "have", "has", "had",
    "having", "do", "does", "did", "doing",
    "a", "an", "the", "and", "but", "if",
    "or", "because", "as", "until", "while",
    "of", "at", "by", "for", "with",
    "about", "against", "between", "into",
    "through", "during", "before", "after",
    "above", "below", "to", "from", "up",
    "down", "in", "out", "on", "off", "over",
    "under", "again", "further", "then",
    "once", "here", "there", "when", "where",
    "why", "how", "all", "any", "both",
    "each", "few", "more", "most", "other",
    "some", "such", "no", "nor", "not",
    "only", "own", "same", "so", "than",
    "too", "very", "s", "t", "can", "will",
    "just", "don", "should", "now"
    ]


# This function has a default input "file.input.txt"
# It will open a file in read return the readed file or return nout find
def open_file(filename=InputFilename):
    try:
        f = open(filename, "r")
        return(f)
    except FileNotFoundError:
        # FileNotFoundError is subclass of OSError
        print('FileNotFound')
        if Debug:
            print("File Not Found")
        return(sys.stdin)
    except OSError:
        if Debug:
            print("Other OS Error")
        return(sys.stdin)


# This method input a file with a constrain "prompt"
# prompt is used for f=None
# If file is not none, method will read it line by line
def safe_input(f=None, prompt=""):
    try:
        # Case:  Stdin
        if f is sys.stdin or f is None:
            line = input(prompt)
        # Case:  From file
        else:
            assert not (f is None)
            assert (f is not None)
            line = f.readline()
            if Debug:
                print("readline: ", line, end='')
            if line == "":  # Check EOF before strip()
                if Debug:
                    print("EOF")
                return("", False)
        return(line.strip(), True)
    except EOFError:
        return("", False)


# Super class, check the type of self.type and id
class C274:
    def __init__(self):
        self.type = str(self.__class__)
        return

    def __str__(self):
        return(self.type)

    def __repr__(self):
        s = "<%d> %s" % (id(self), self.type)
        return(s)


# Hides details of classification strategy and metrics of output
class ClassifyByTarget(C274):
    def __init__(self, lw=[]):
        super().__init__()      # Call superclass
        # self.type = str(self.__class__)
        self.allWords = 0
        self.theCount = 0
        self.nonTarget = []
        self.set_target_words(lw)
        self.initTF()
        return

    def initTF(self):
        self.TP = 0
        self.FP = 0
        self.TN = 0
        self.FN = 0
        return

    # FIXME:  Incomplete.  Finish get_TF() and other getters/setters.
    def get_TF(self):
        return(self.TP, self.FP, self.TN, self.FN)

    # TODO: Could use Use Python properties
    #     https://www.python-course.eu/python3_properties.php
    def set_target_words(self, lw):
        # Could also do self.targetWords = lw.copy().  Thanks, TA Jason Cannon
        self.targetWords = copy.deepcopy(lw)
        return

    def get_target_words(self):
        return(self.targetWords)

    def get_allWords(self):
        return(self.allWords)

    def incr_allWords(self):
        self.allWords += 1
        return

    def get_theCount(self):
        return(self.theCount)

    def incr_theCount(self):
        self.theCount += 1
        return

    def get_nonTarget(self):
        return(self.nonTarget)

    def add_nonTarget(self, w):
        self.nonTarget.append(w)
        return

    def print_config(self, printSorted=True):
        print("-------- Print Config --------")
        ln = len(self.get_target_words())
        print("TargetWords (%d): " % ln, end='')
        if printSorted:
            print(sorted(self.get_target_words()))
        else:
            print(self.get_target_words())
        return

    def print_run_info(self, printSorted=True):
        print("-------- Print Run Info --------")
        print("All words:%3s. " % self.get_allWords(), end='')
        print(" Target words:%3s" % self.get_theCount())
        print("Non-Target words (%d): " % len(self.get_nonTarget()), end='')
        if printSorted:
            print(sorted(self.get_nonTarget()))
        else:
            print(self.get_nonTarget())
        return

    def print_confusion_matrix(self, targetLabel, doKey=False, tag=""):
        assert (self.TP + self.TP + self.FP + self.TN) > 0
        print(tag+"-------- Confusion Matrix --------")
        print(tag+"%10s | %13s" % ('Predict', 'Label'))
        print(tag+"-----------+----------------------")
        print(tag+"%10s | %10s %10s" % (' ', targetLabel, 'not'))
        if doKey:
            print(tag+"%10s | %10s %10s" % ('', 'TP   ', 'FP   '))
        print(tag+"%10s | %10d %10d" % (targetLabel, self.TP, self.FP))
        if doKey:
            print(tag+"%10s | %10s %10s" % ('', 'FN   ', 'TN   '))
        print(tag+"%10s | %10d %10d" % ('not', self.FN, self.TN))
        return

    # Note tset is TraningSet
    def eval_training_set(self, tset, targetLabel, lines=True):
        print("-------- Evaluate Training Set --------")
        self.initTF()
        # zip is good for parallel arrays and iteration
        z = zip(tset.get_instances(), tset.get_lines())
        for ti, w in z:
            lb = ti.get_label()
            cl = ti.get_class()
            if lb == targetLabel:
                if cl:
                    self.TP += 1
                    outcome = "TP"
                else:
                    self.FN += 1
                    outcome = "FN"
            else:
                if cl:
                    self.FP += 1
                    outcome = "FP"
                else:
                    self.TN += 1
                    outcome = "TN"
            explain = ti.get_explain()
            # Format nice output
            if lines:
                w = ' '.join(w.split())
            else:
                w = ' '.join(ti.get_words())
                w = lb + " " + w

            # TW = testing bag of words words (kinda arbitrary)
            print("TW %s: ( %10s) %s" % (outcome, explain, w))
            if Debug:
                print("-->", ti.get_words())
        self.print_confusion_matrix(targetLabel)
        return

    def classify_by_words(self, ti, update=False, tlabel="last"):
        inClass = False
        evidence = ''
        lw = ti.get_words()
        for w in lw:
            if update:
                self.incr_allWords()
            if w in self.get_target_words():    # FIXME Write predicate
                inClass = True
                if update:
                    self.incr_theCount()
                if evidence == '':
                    evidence = w            # FIXME Use first word, but change
            elif w != '':
                if update and (w not in self.get_nonTarget()):
                    self.add_nonTarget(w)
        if evidence == '':
            evidence = '#negative'
        if update:
            ti.set_class(inClass, tlabel, evidence)
        return(inClass, evidence)

    # Could use a decorator, but not now
    def classify(self, ti, update=False, tlabel="last"):
        cl, e = self.classify_by_words(ti, update, tlabel)
        return(cl, e)

    # This method pass "ts" from training set
    # and "classify" them, return two variable
    def classify_all(self, ts, update=True, tlabel="classify_all"):
        for ti in ts.get_instances():
            cl, e = self.classify(ti, update=update, tlabel=tlabel)
        return


class ClassifyByTopN(ClassifyByTarget):
    def __init__(self, lw=TargetWords):
        super().__init__()
        self.set_target_words(lw)
        self.num = []

    def target_top_n(self, tset, num=5, label=''):
        count = {}
        stopped_word = []
        word_list = []
        wdnmd = tset.get_instances()
        for i in wdnmd:
            sentence = ' '.join(i.get_words())
            lb = i.get_label()
            if lb == label:
                for i in sentence.split():
                    if i not in word_list:
                        word_list.append(i)
                        count[i] = 1
                    elif i in word_list:
                        count[i] += 1
        val = count.values()
        val = sorted(val)
        cFlag = True
        while cFlag:
            if val[-num] == val[-num-1]:
                num += 1
            else:
                cFlag = False
        for i in count:
            if count[i] in val[-num:]:
                stopped_word.append(i)
        self.set_target_words(sorted(stopped_word))


# Hides details of Bag of Words
class TrainingInstance(C274):
    def __init__(self):
        super().__init__()              # Call superclass
        # self.type = str(self.__class__)
        self.inst = dict()
        # FIXME:  Get rid of dict, and use attributes
        self.inst["label"] = "N/A"      # Class, given by oracle
        self.inst["words"] = []         # Bag of words
        self.inst["class"] = ""         # Class, by classifier
        self.inst["explain"] = ""       # Explanation for classification
        self.inst["experiments"] = dict()   # Previous classifier runs
        return

    # This part write by student
    def preprocess_words(self, sentence, mode=''):
        # This part check the optional command line argument
        m_line = self.preprocess(sentence, mode)
        m_line = m_line.split()
        return(m_line)

    # Belone to preprocess_words
    # require an input text and an optional command line argument
    # and will output the preprocessed text
    def preprocess(self, sentence, mode=''):
        # This part convert to lowercase
        text = sentence.lower()
        text = text.split()

        # This part will decide to remove non-alphabet elements
        # with respect to optional command line argument
        alpha = []
        for i in text[:]:
            if i.isalpha():
                alpha.append(i)
            elif i.isnumeric():
                alpha.append(i)
            else:
                newword = ''
                non_alpha = i
                fig_check = ''
                for j in non_alpha[:]:
                    if self.no_symbol(j, mode) is True:
                        fig_check += j
                for j in non_alpha[:]:
                    if (self.mode_option(j, mode) is True and
                            not fig_check.isnumeric()):
                        newword += j
                    elif fig_check.isnumeric():
                        newword = fig_check
                if newword != '':
                    alpha.append(newword)

        # This part remove stopword from the text
        stopped_char = []
        condi = False
        for i in alpha:
            if mode == 'keep-stops':
                break
            if i in Stop_Words:
                stopped_char.append(i)
                condi = True
        if condi is True:
            for i in range(len(stopped_char)):
                alpha.remove(stopped_char[i])
        # This part output the preprocessed text
        if len(alpha) > 0:
            for i in alpha:
                line = ' '.join(alpha)
        else:
            line = ''
        return(line)

    # belong to preprocess_words
    # mode_option will recognize the optional command line argument
    # and implement the correct action
    def mode_option(self, j, mode):
        if (mode == '' or mode == 'keep-stops'):
            if j.isalpha():
                return(True)
        elif mode == 'keep-digits':
            if j.isalpha() or j.isnumeric():
                return(True)
        elif mode == 'keep-symbols':
            if not j.isnumeric():
                return(True)

    # belong to preprocess_words
    # no_symbol function will remove all sumbols
    # except optional command line argument is 'keep-symbols'
    def no_symbol(self, j, mode):
        if j.isalpha() or j.isnumeric() and mode != 'keep-symbols':
            return(True)
        elif mode == 'keep-symbols':
            return(False)

    def set_words(self, n_words):
        self.inst["words"] = n_words
        return

    def get_label(self):
        return(self.inst["label"])

    def get_words(self):
        return(self.inst["words"])

    def set_class(self, theClass, tlabel="last", explain=""):
        # tlabel = tag label
        self.inst["class"] = theClass
        self.inst["experiments"][tlabel] = theClass
        self.inst["explain"] = explain
        return

    def get_class_by_tag(self, tlabel):             # tlabel = tag label
        cl = self.inst["experiments"].get(tlabel)
        if cl is None:
            return("N/A")
        else:
            return(cl)

    def get_explain(self):
        cl = self.inst.get("explain")
        if cl is None:
            return("N/A")
        else:
            return(cl)

    def get_class(self):
        return self.inst["class"]

    def process_input_line(
                self, line, run=None,
                tlabel="read", inclLabel=False
            ):

        for w in line.split():
            if w[0] == "#":
                self.inst["label"] = w
                if inclLabel:
                    # This code append the label after # from text
                    self.inst["words"].append(w)
            else:
                # This code append the words after label
                self.inst["words"].append(w)
        if not (run is None):
            cl, e = run.classify(self, update=True, tlabel=tlabel)
        return(self)


# Hides details of dataset, pass classifier as a parameter to TrainingInstance
class TrainingSet(C274):
    def __init__(self):
        super().__init__()      # Call superclass
        # self.type = str(self.__class__)
        self.inObjList = []     # Unparsed lines, from training set
        self.inObjHash = []     # Parsed lines, in dictionary/hash
        self.variable = dict()  # NEW: Configuration/environment variables
        return

    def preprocess(self, mode=''):
        # FIXME 老东西肯定要整活
        wtmll = self.get_instances()
        for i in wtmll:
            sentence = ' '.join(i.get_words())
            start = TrainingInstance()
            n_line = start.preprocess_words(sentence, mode)
            i.set_words(n_line)
        return

    def return_nfolds(self, num=3):
        # FIXME wrote by student
        z = zip(self.get_instances(), self.inObjList)
        inObjHash = []
        inObjList = []
        Result_list = []
        for i in range(num):
            inObjHash.append([])
            inObjList.append([])
        k = 0
        for i, j in z:
            inObjHash[k].append(i)
            inObjList[k].append(j)
            k += 1
            if k == num:
                k = 0
        N_data = self.copy()
        for i in range(num):
            N_data.inObjHash = inObjHash[i]
            N_data.inObjList = inObjList[i]
            Result_list.append(self.deepcopy(N_data))
        return(Result_list)

    def copy(self):
        N_data = copy.deepcopy(self)
        return(N_data)

    def deepcopy(self, tset):
        N_data = copy.deepcopy(tset)
        return(N_data)

    def add_training_set(self, tset):
        temp_list1 = []
        temp_list2 = []
        z1 = zip(self.inObjHash, self.inObjList)
        for i, j in z1:
            temp_list1.append(i)
            temp_list2.append(j)
        z2 = zip(tset.inObjHash, tset.inObjList)
        for i, j in z2:
            temp_list1.append(i)
            temp_list2.append(j)
        self.inObjHash = copy.deepcopy(temp_list1)
        self.inObjList = copy.deepcopy(temp_list2)
        return

    def test_data(self, tset):
        print('T0', len(tset.inObjList))
        for i in tset.inObjHash:
            print(i.get_words())
        return

    def set_env_variable(self, k, v):
        self.variable[k] = v
        return

    def get_env_variable(self, k):
        if k in self.variable:
            return(self.variable[k])
        else:
            return ""

    # This method add a new env_variable, triggered by following condi
    def inspect_comment(self, line):
        if len(line) > 1 and line[1] != ' ':      # Might be variable
            v = line.split(maxsplit=1)
            self.set_env_variable(v[0][1:], v[1])
        return

    # inObjHash only record the type of inObjHash
    def get_instances(self):
        return(self.inObjHash)      # FIXME Should protect this more

    # inObjList record the lines behind target words
    def get_lines(self):
        return(self.inObjList)      # FIXME Should protect this more

    def print_training_set(self):
        print("-------- Print Training Set --------")
        z = zip(self.inObjHash, self.inObjList)
        for ti, w in z:
            lb = ti.get_label()
            cl = ti.get_class_by_tag("last")     # Not used
            explain = ti.get_explain()
            print("( %s) (%s) %s" % (lb, explain, w))
            if Debug:
                print("-->", ti.get_words())
        return

    # This method will check % and test whether it is an env_variable
    def process_input_stream(self, inFile, run=None):
        assert not (inFile is None), "Assume valid file object"
        cFlag = True
        while cFlag:
            line, cFlag = safe_input(inFile)
            if not cFlag:
                break
            assert cFlag, "Assume valid input hereafter"
            if len(line) == 0:   # Blank line.  Skip it.
                continue
            # Check for comments *and* environment variables
            if line[0] == '%':  # Comments must start with % and variables
                self.inspect_comment(line)
                continue
            # Save the training data input, by line
            self.inObjList.append(line)
            # Save the training data input, after parsing
            ti = TrainingInstance()
            ti.process_input_line(line, run=run)
            # inObjHash exist as a list of dictionary
            self.inObjHash.append(ti)
        return


# Very basic test of functionality
def basemain():
    global Debug
    tset = TrainingSet()
    run1 = ClassifyByTarget(TargetWords)
    if Debug:
        print(run1)     # Just to show __str__
        lr = [run1]
        print(lr)       # Just to show __repr__

    argc = len(sys.argv)
    if argc == 1:   # Use stdin, or default filename
        inFile = open_file()
        assert not (inFile is None), "Assume valid file object"
        tset.process_input_stream(inFile, run1)
        inFile.close()
    else:
        for f in sys.argv[1:]:
            # Allow override of Debug from command line
            if f == "Debug":
                Debug = True
                continue
            if f == "NoDebug":
                Debug = False
                continue

            inFile = open_file(f)
            assert not (inFile is None), "Assume valid file object"
            tset.process_input_stream(inFile, run1)
            inFile.close()

    print("--------------------------------------------")
    plabel = tset.get_env_variable("pos-label")
    print("pos-label: ", plabel)
    print("NOTE: Not using any target words from the file itself")
    print("--------------------------------------------")

    if Debug:
        tset.print_training_set()
    run1.print_config()
    run1.print_run_info()
    run1.eval_training_set(tset, plabel)


if __name__ == "__main__":
    basemain()
