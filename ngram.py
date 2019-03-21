# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 16:20:04 2019

@author: Barış
"""
import math
from math import pow
from random import randint

def ngram(n):
    trainFile = open("brown.train.txt","r")  
    global words,wordsLen,uniqueWords,uniqueWordsCount
    words = trainFile.read().split(' ')
    wordsLen = len(words)
    
    uniqueWords = []
    uniqueWordsCount = []
    
    for i in range(0,wordsLen-n+1):
        
        tempWord = words[i]
        for k in range(1,n):
            tempWord = tempWord + " " + words[i + k]
        
        if(tempWord in uniqueWords):
            tempIndex = uniqueWords.index(tempWord)
            uniqueWordsCount[tempIndex] = uniqueWordsCount[tempIndex] + 1
        else:
            uniqueWords.append(tempWord)
            uniqueWordsCount.append(1)
    
    return [uniqueWords,uniqueWordsCount]
        
    #    if tempWord not in uniqueWords:
    #        uniqueWords.append(tempWord)
    #        uniqueWordsCount.append(words.count(tempWord))
        
def prob(exampleSentence,n):
    exampleWords = exampleSentence.split(" ")
    exampleWordsLen = len(exampleWords)    
    mle = 1
    for i in range(0,exampleWordsLen-n+1):
        
        tempWord = exampleWords[i]
        for k in range(1,n):
            tempWord = tempWord + " " + exampleWords[i + k]
        if n == 1:
            if (tempWord not in unigram[0]):
                mle = 0
            else:
                mle = mle * unigram[1][unigram[0].index(tempWord)] / sum(unigram[1])
        if n == 2:
            if (tempWord not in bigram[0]):
                mle = 0
            else:
                splittedTemp = tempWord.split(" ")
                mle = mle * bigram[1][bigram[0].index(tempWord)] / unigram[1][unigram[0].index(splittedTemp[0])]
        if n == 3:
            if (tempWord not in trigram[0]):
                mle = 0
            else:
                splittedTemp = tempWord.split(" ")
                tempSplitted = splittedTemp[0] + " " + splittedTemp[1]
                mle = mle * trigram[1][trigram[0].index(tempWord)] / bigram[1][bigram[0].index(tempSplitted)]
    
    return mle

def ppl(exampleSentence,n,probType):
    splittedSentences = exampleSentence.split("''")
    curPPL = 0
    if probType == 1:
        for i in range(0,len(splittedSentences)):
            curPPL = curPPL + math.log2(prob(splittedSentences[i],n))
    elif probType == 2:
        for i in range(0,len(splittedSentences)):
            curPPL = curPPL + math.log2(sprob(splittedSentences[i],n))
    elif probType == 3:
        for i in range(0,len(splittedSentences)):
            curPPL = curPPL + math.log2(linearInterpolation(splittedSentences[i],n))
    elif probType == 4:
        for i in range(0,len(splittedSentences)):
            curPPL = curPPL + math.log2(discounting(splittedSentences[i],n))
            
    curPPL = 1/len(exampleSentence) * curPPL
    curPPL = math.pow(2,-curPPL)
    return curPPL

def sprob(exampleSentence,n):
    exampleWords = exampleSentence.split(" ")
    exampleWordsLen = len(exampleWords)    
    mle = 1
    for i in range(0,exampleWordsLen-n+1):
        
        tempWord = exampleWords[i]
        for k in range(1,n):
            tempWord = tempWord + " " + exampleWords[i + k]
        if n == 1:
            if (tempWord not in unigram[0]):
                mle = 1/ (sum(unigram[1]) + len(unigram[0]))
            else:
                mle = mle * (unigram[1][unigram[0].index(tempWord)] + 1 )/ (sum(unigram[1]) + len(unigram[0]))
        if n == 2:
            if (tempWord not in bigram[0]):
                mle = 1/ (sum(bigram[1]) + len(bigram[0]))
            else:
                splittedTemp = tempWord.split(" ")
                mle = mle * (bigram[1][bigram[0].index(tempWord)] + 1) / (unigram[1][unigram[0].index(splittedTemp[0])] + len(bigram[0]))
        if n == 3:
            if (tempWord not in trigram[0]):
                mle = 1 / (sum(trigram[1]) + len(trigram[0]))
            else:
                splittedTemp = tempWord.split(" ")
                tempSplitted = splittedTemp[0] + " " + splittedTemp[1]
                mle = mle * (trigram[1][trigram[0].index(tempWord)] + 1) / (bigram[1][bigram[0].index(tempSplitted)] + len(trigram[0]))
    return mle

def nextWord(words,wordPos,n):
    if(wordPos > 20):
        return words
    else:
        if(n == 1):
            wordToAdd = uniqueWords[randint(0,len(uniqueWords)-1)]
        else:
            splittedWords = words.split(" ")
            wordsOfInterest = splittedWords[-1]
            for k in range(2,n):
                wordsOfInterest = wordsOfInterest + " " + splittedWords[-n+1]
            newWord = []
            for i in range(0,len(uniqueWordsCount)):
                fromList = uniqueWords[i].split(" ")
                tempWord = fromList[-2]
                for k in range(2,n):
                    tempWord = tempWord + " " + fromList[-n]
                    
                if (tempWord == wordsOfInterest) and (uniqueWordsCount[i] > 0) and not fromList[-1] == "''":
                    newWord.append(fromList[-1])
            if(len(newWord) == 1):
                wordToAdd = newWord[0]
            elif (len(newWord) == 0):
                wordToAdd = "."
            else:
                wordToAdd = newWord[randint(0,len(newWord)-1)]
        
        if(wordToAdd[0] == "." or "/n" in wordToAdd):
            return words
        else:
            wordPos = wordPos + 1
            words = words + " " + wordToAdd
            return nextWord(words,wordPos,n)

def findBeginning(n):
    beginningSentences = []
    if n == 1:
        uniqueWords = unigram[0]
    elif n == 2:
        uniqueWords = bigram[0]
    elif n == 3:
        uniqueWords = trigram[0]
        
    for i in range(0,len(uniqueWords)):
        if(uniqueWords[i][0] == "."):
            beginningSentences.append(uniqueWords[i])
    return beginningSentences

def printNPL(sentence,n):
    print("Sentence: " + sentence)
    print("MLE: " + str(prob(sentence,n)))
    
def linearInterpolation(exampleSentence,n):
    
    if n == 3:
        lambda1 = 1/3
        lambda2 = 1/3
        lambda3 = 1 - lambda1 - lambda2
        return lambda1 * sprob(exampleSentence,3) + lambda2 * sprob(exampleSentence,2) + lambda3 * sprob(exampleSentence,1)
    elif n == 2:
        lambda1 = 1/2
        lambda2 = 1 - lambda1
        return lambda1 * sprob(exampleSentence,2) + lambda2 * sprob(exampleSentence,1)
def linearInterpolationOptimization():
    lambda1 = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    lambda2 = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    maxProb = 0
    trainFile = open("brown.dev.txt","r")  
    words = trainFile.read().split(' ')
    if n == 3:
        maxLambda1 = 0
        maxLambda2 = 0
        for i in range(0,10):
            for k in range(0,10):
                if lambda1[i] + lambda2[k] < 1:
                    lambda3 = 1 - lambda1[i] - lambda2[k]
                    tempProb = lambda1[i] * sprob(words,3) + lambda2[k] * sprob(words,2) + lambda3 * sprob(words,1)
                    if tempProb > maxProb:
                        maxProb = tempProb
                        maxLambda1 = lambda1[i]
                        maxLambda2 = lambda2[k]
        return [maxLambda1,maxLambda2]
    if n == 2:
        maxLambda1 = 0
        for i in range(0,10):
            lambda2 = 1 - lambda1[i]
            tempProb = lambda1[i] * sprob(words,2) + lambda2 * sprob(words,1)
            if tempProb > maxProb:
                maxProb = tempProb
                maxLambda1 = lambda1[i]
        return maxLambda1
                
def discountingOptimization():
    
    betaValues = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    maxProb = 0
    maxBeta = 0
    for j in range(0,10):
        trainFile = open("brown.dev.txt","r")  
        exampleWords = trainFile.read().split(' ')
        for i in range(0,exampleWordsLen-n+1):
            beta = betaValues[j]
            tempWord = exampleWords[i]
            for k in range(1,n):
                tempWord = tempWord + " " + exampleWords[i + k]
            if n == 1:
                if (tempWord not in unigram[0]):
                    mle = 0
                else:
                    mle = mle * (unigram[1][unigram[0].index(tempWord)] - beta) / sum(unigram[1])
            if n == 2:
                if (tempWord not in bigram[0]):
                    curWord = tempWord.split(" ")[0]
                    count = 0
                    for k in range(0,len(bigram[0])):
                        tempBigram = bigram[0][k].split(" ")[0]
                        if tempBigram == curWord:
                            count = count + 1
                    if curWord in unigram[1]:
                        alpha = count * beta / unigram[1][unigram[0].index(curWord)]
                        mle = mle * alpha * prob(curWord,1)
                else:
                    splittedTemp = tempWord.split(" ")
                    mle = mle * (bigram[1][bigram[0].index(tempWord)] - beta) / unigram[1][unigram[0].index(splittedTemp[0])]
            if n == 3:
                if (tempWord not in trigram[0]):
                    curWord = tempWord.split(" ")[0] + " " + tempWord.split(" ")[1]
                    count = 0
                    for k in range(0,len(bigram[0])):
                        tempBigram = trigram[0][k].split(" ")[0] + " " + trigram[0][k].split(" ")[1]
                        if tempBigram == curWord:
                            count = count + 1
                    if curWord in bigram[1]:         
                        alpha = count * beta / bigram[1][bigram[0].index(curWord)]
                        mle = mle * alpha * prob(curWord,2)
                else:
                    splittedTemp = tempWord.split(" ")
                    tempSplitted = splittedTemp[0] + " " + splittedTemp[1]
                    mle = mle * (trigram[1][trigram[0].index(tempWord)] - beta) / bigram[1][bigram[0].index(tempSplitted)]
            if mle > maxProb:
                maxProb = mle
                maxBeta = beta
        return maxBeta
    
def discounting(exampleSentence,n):
    exampleWords = exampleSentence.split(" ")
    exampleWordsLen = len(exampleWords)    
    mle = 1

    for i in range(0,exampleWordsLen-n+1):
        beta = 0.5
        tempWord = exampleWords[i]
        for k in range(1,n):
            tempWord = tempWord + " " + exampleWords[i + k]
        if n == 1:
            if (tempWord not in unigram[0]):
                mle = 0
            else:
                mle = mle * (unigram[1][unigram[0].index(tempWord)] - beta) / sum(unigram[1])
        if n == 2:
            if (tempWord not in bigram[0]):
                curWord = tempWord.split(" ")[0]
                count = 0
                for k in range(0,len(bigram[0])):
                    tempBigram = bigram[0][k].split(" ")[0]
                    if tempBigram == curWord:
                        count = count + 1
                if curWord in unigram[1]:
                    alpha = count * beta / unigram[1][unigram[0].index(curWord)]
                    mle = mle * alpha * prob(curWord,1)
            else:
                splittedTemp = tempWord.split(" ")
                mle = mle * (bigram[1][bigram[0].index(tempWord)] - beta) / unigram[1][unigram[0].index(splittedTemp[0])]
        if n == 3:
            if (tempWord not in trigram[0]):
                curWord = tempWord.split(" ")[0] + " " + tempWord.split(" ")[1]
                count = 0
                for k in range(0,len(bigram[0])):
                    tempBigram = trigram[0][k].split(" ")[0] + " " + trigram[0][k].split(" ")[1]
                    if tempBigram == curWord:
                        count = count + 1
                if curWord in bigram[1]:         
                    alpha = count * beta / bigram[1][bigram[0].index(curWord)]
                    mle = mle * alpha * prob(curWord,2)
            else:
                splittedTemp = tempWord.split(" ")
                tempSplitted = splittedTemp[0] + " " + splittedTemp[1]
                mle = mle * (trigram[1][trigram[0].index(tempWord)] - beta) / bigram[1][bigram[0].index(tempSplitted)]
    
    return mle
    
unigram = ngram(1)
bigram = ngram(2)
trigram = ngram(3)

testFile = open("brown.test.txt","r")
testFileSentence = testFile.read()
    
for n in range(1,4):

#    print("Perplexity of given test by MLE file in " + str(n) + "gram: " + str(ppl(testFileSentence,n,1)))
    print("Perplexity of given test by Smoothed MLE file in " + str(n) + "gram: " + str(ppl(testFileSentence,n,2)))
    if n > 2:
        print("Perplexity of given test by Linear Interpolation file in " + str(n) + "gram: " + str(ppl(testFileSentence,n,3)))
        print("Perplexity of given test by Discounting file in " + str(n) + "gram: " + str(ppl(testFileSentence,n,4))) 
    
    beginningSentences = findBeginning(n)
    sentence1 = nextWord(beginningSentences[randint(0,len(beginningSentences)-1)],n,n)
    sentence2 = nextWord(beginningSentences[randint(0,len(beginningSentences)-1)],n,n)
    sentence3 = nextWord(beginningSentences[randint(0,len(beginningSentences)-1)],n,n)
    sentence4 = nextWord(beginningSentences[randint(0,len(beginningSentences)-1)],n,n)
    sentence5 = nextWord(beginningSentences[randint(0,len(beginningSentences)-1)],n,n)
    
    print("For n = " + str(n))
    print("Sentence1: ")
    printNPL(sentence1,n)
    
    print("Sentence2: ")
    printNPL(sentence2,n)
    
    print("Sentence3: ")
    printNPL(sentence3,n)
    
    print("Sentence4: ")
    printNPL(sentence4,n)
    
    print("Sentence5: ")
    printNPL(sentence5,n)
    

 


