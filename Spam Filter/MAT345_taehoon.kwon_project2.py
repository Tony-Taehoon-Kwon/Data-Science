# Start Header -------------------------------------------------------
#Copyright (C) 2019 DigiPen Institute of Technology.
#Reproduction or disclosure of this file or its contents without the prior written
#consent of DigiPen Institute of Technology is prohibited.
#Author: Taehoon Kwon (180003118)
#Email : taehoon.kwon@digipen.edu
#Course : MAT
#Section : 345
#Semester : Fall 2019
#File Name: MAT345_taehoon.kwon_project2.py
#Language: Python
#Platform: Visual Studio 2017, Windows 10
#Creation date: Oct/21/2019
#End Header --------------------------------------------------------

# import os, shutil, Path module
from pathlib import Path
import os, shutil

def fourth_file_move_dir(src: str, dst: str, pattern: str = '*'):
    if not os.path.isdir(dst):
        Path(dst).mkdir(parents=True, exist_ok=True)
    for f in os.listdir(src):
        fileName = Path(f).resolve().stem
        if int(fileName) % 4 == 0:
            shutil.move(os.path.join(src, f), os.path.join(dst, f))
    return

def split_data():
    easy_ham_path = Path("easy_ham/")
    hard_ham_path = Path("hard_ham/")
    spam_path = Path("spam/")
    testing_path = Path("testing/")

    fourth_file_move_dir(easy_ham_path.name, testing_path.name + "/easy_ham/", '*')
    fourth_file_move_dir(hard_ham_path.name, testing_path.name + "/hard_ham/", '*')
    fourth_file_move_dir(spam_path.name, testing_path.name + "/spam/", '*')
    return

def removeSymbols(word: str):
    word = word.replace('~', '').replace('!', '').replace('@', '').replace('#', '')
    word = word.replace('^', '').replace('*', '').replace('(', '').replace(')', '')
    word = word.replace('-', '').replace('_', '').replace('+', '').replace('=', '')
    word = word.replace(':', '').replace(';', '').replace('\'', '').replace('\"', '')
    word = word.replace('`', '').replace('<', '').replace('>', '').replace(',', '')
    word = word.replace('.', '').replace('/', '').replace('?', '').replace('{', '')
    word = word.replace('}', '').replace('[', '').replace(']', '').replace('\\', '')
    word = word.replace('|', '')
    return word

def prepositionCheck(word: str):
    if (word.lower() == "of"         or word.lower() == "with"    or
        word.lower() == "at"         or word.lower() == "from"    or
        word.lower() == "into"       or word.lower() == "during"  or
        word.lower() == "including"  or word.lower() == "until"   or
        word.lower() == "against"    or word.lower() == "among"   or
        word.lower() == "throughout" or word.lower() == "despite" or
        word.lower() == "towards"    or word.lower() == "upon"    or
        word.lower() == "to"         or word.lower() == "in"      or
        word.lower() == "for"        or word.lower() == "on"      or
        word.lower() == "by"         or word.lower() == "about"   or
        word.lower() == "through"    or word.lower == "over"      or
        word.lower() == "before"     or word.lower == "between"   or
        word.lower() == "after"      or word.lower == "since"     or
        word.lower() == "without"    or word.lower == "under"     or
        word.lower() == "within"     or word.lower == "along"     or
        word.lower() == "behind"     or word.lower == "beyond"    or
        word.lower() == "except"     or word.lower == "but"       or
        word.lower() == "up"         or word.lower == "out"       or
        word.lower() == "around"     or word.lower == "down"      or
        word.lower() == "off"        or word.lower == "above"):
        return True
    return False

def unnecessaryWordCheck(word: str):
    if (prepositionCheck(word)    or 
        word.lower() == "subject" or word.lower() == "re"  or
        word.lower() == "the"     or word.lower() == "a"   or
        word.lower() == "and"     or word.lower() == "was" or
        word.lower() == "or"      or word.lower() == "an"):
        return True
    return False

def read_file_training(src: str, numCount: dict):
    numOfMsgs = 0
    for f in os.listdir(src):
        numOfMsgs += 1
        file = open(src.name + '/' + f, "rt", encoding='utf-8', errors='ignore')
        if (file.mode == "rt"):
            lines = file.readlines()
            for line in lines:                           # for each line
                if "Subject:" in line:                   # if the line has word "Subject"
                    for word in line.split():            # then split that line into words
                        word = removeSymbols(word)       # remove symbols attached to the word
                        if (unnecessaryWordCheck(word)): # if the word is unnecessary, skip
                            continue
                        allWords.add(word.lower())       # otherwise, store the word in lowercase
                        numCount[word.lower()] = numCount.get(word.lower(), 0.0) + 1.0
    return numOfMsgs

def trainingData():
    easy_ham_path = Path("easy_ham/")
    hard_ham_path = Path("hard_ham/")
    spam_path     = Path("spam/")

    messageCount['ham']  += read_file_training(easy_ham_path, hamWordsCount)
    messageCount['ham']  += read_file_training(hard_ham_path, hamWordsCount)
    messageCount['spam'] += read_file_training(spam_path,     spamWordsCount)
    return

def read_file_testing(src: str):
    for f in os.listdir(src):
        a_vector.clear()
        path = 'testing/' + src.name + '/' + f
        file = open(path, "rt", encoding='utf-8', errors='ignore')
        if (file.mode == "rt"):
            lines = file.readlines()
            for line in lines:                           # for each line
                if "Subject:" in line:                   # if the line has word "Subject"
                    for word in line.split():            # then split that line into words
                        word = removeSymbols(word)       # remove symbols attached to the word
                        count = 0
                        for keyWord in testingKeyword:   # for selected high probabilty words
                            if word.lower() == keyWord:  # if the new message word matches with keyword
                                a_vector.append((keyWord, 1)) # then, label as 1
                            else:
                                a_vector.append((keyWord, 0)) # otherwise, label as 0
            spam_intermediate = 1.0
            ham_intermediate  = 1.0
            for a_k in a_vector:                # calculating P(spam|X_vec=a_vec) in this loop
                spamProb = 0.0
                hamProb  = 0.0
                if a_k[1] == 1: # if the word w_k is in the new message
                    spamProb = (spamWordsCount.get(a_k[0], 0.0) + 1) / (messageCount['spam'] + 2)
                    hamProb  = (hamWordsCount.get(a_k[0], 0.0)  + 1) / (messageCount['ham']  + 2)
                else:
                    spamProb = (1 - (spamWordsCount.get(a_k[0], 0.0) + 1) / (messageCount['spam'] + 2))
                    hamProb  = (1 - (hamWordsCount.get(a_k[0], 0.0)  + 1) / (messageCount['ham']  + 2))
                spam_intermediate *= spamProb
                ham_intermediate  *= hamProb
            spam_intermediate *= p_spam
            ham_intermediate  *= p_ham
            testingResult.append((path, spam_intermediate / (spam_intermediate + ham_intermediate)))
    return

def testingData():
    testing_easy_ham_path = Path("testing/easy_ham/")
    testing_hard_ham_path = Path("testing/hard_ham/")
    testing_spam_path     = Path("testing/spam/")

    read_file_testing(testing_easy_ham_path)
    read_file_testing(testing_hard_ham_path)
    read_file_testing(testing_spam_path)    
    return

# if the given set data are not split into separte folders,
# then uncomment the code below
#split_data()

# initialize variables
messageCount       = {"spam": 0, "ham": 0}
allWords           = set()
spamWordsCount     = {}
hamWordsCount      = {}
smoothingSpamProb  = []
smoothingHamProb   = []
a_vector           = []
testingResult      = []
testingKeyword     = set()

# train the data
trainingData()

# calculate p(spam) and p(ham)
p_spam = messageCount['spam'] / (messageCount['spam'] + messageCount['ham'])
p_ham  = messageCount['ham']  / (messageCount['spam'] + messageCount['ham'])

# calculate p(spam|w_k) and p(ham|w_k)
for word in allWords:
    spamProb = (spamWordsCount.get(word, 0.0) + 1) / (messageCount['spam'] + 2)
    hamProb  = (hamWordsCount.get(word, 0.0)  + 1) / (messageCount['ham']  + 2)
    p_spam_w_k = spamProb*p_spam / (spamProb*p_spam + hamProb*p_ham)
    p_ham_w_k  = hamProb*p_ham   / (spamProb*p_spam + hamProb*p_ham)
    smoothingSpamProb.append((word, p_spam_w_k))
    smoothingHamProb.append((word, p_ham_w_k))
    
# sort the probability in descending order
smoothingSpamProb.sort(key = lambda pair: pair[1], reverse = True)
smoothingHamProb.sort(key = lambda pair: pair[1], reverse = True)

# print 5 most spammiest word
print("[5 Highest probabilities of P(spam|w_k)]")
count = 0
for prob in smoothingSpamProb:
    count += 1
    if count <= 5:
        print(prob[0] + ' : ' + str(prob[1]))
    if count > 50:
        break    
    testingKeyword.add(prob[0])

# print 5 most hammiest word
print("\n")
print("[5 Highest probabilities of P(ham|w_k)]")
count = 0
for prob in smoothingHamProb:
    count += 1
    if count <= 5:
        print(prob[0] + ' : ' + str(prob[1]))
    if count > 50:
        break
    testingKeyword.add(prob[0])

# test the new message
testingData()

# initialize variables
predict_spam_in_spam = 0
predict_spam_in_ham  = 0
predict_ham_in_spam  = 0
predict_ham_in_ham   = 0

for result in testingResult:
    if "spam" in result[0]:
        if result[1] >= 0.5:
            predict_spam_in_spam += 1
        else:
            predict_ham_in_spam  += 1
    elif "ham" in result[0]:
        if result[1] >= 0.5:
            predict_spam_in_ham  += 1
        else:
            predict_ham_in_ham   += 1

# calculate the accuracy, precision, and recall value
accuracy  = (predict_spam_in_spam + predict_ham_in_ham) / (predict_spam_in_spam + predict_spam_in_ham + predict_ham_in_spam + predict_ham_in_ham)
precision = predict_spam_in_spam / (predict_spam_in_spam + predict_spam_in_ham)
recall    = predict_spam_in_spam / (predict_spam_in_spam + predict_ham_in_spam)

print("\n")
print("accuracy : "  + str(accuracy))
print("precision : " + str(precision))
print("recall : "    + str(recall))
