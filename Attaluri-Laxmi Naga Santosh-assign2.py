from builtins import range
from collections import defaultdict
import numpy
from random import shuffle
import math
import copy

f = open('berp-POS-training.txt', 'r')
stringg = f.read()
file = stringg.split('\n')
# print(len(file))
#file = file[:3000]
print(len(file))

list1 = []  # contains all the list of unique tags
temp1 = []  # contains all the words in the format ['number','word','tag']
map1 = {}  # contains all the tags and the corresponding counts
sentences = []  # contains a list of sentences

temp_sent = []  # temporary sentences # Basically the below for loop writes the sentences into an array(of sentences)
for i in file:
    if (len(i) > 1):
        temp_sent.append(i);
    else:
        sentences.append(temp_sent)
        temp_sent = []

#####################################################################
shuffle(sentences)
print(sentences)
words_list = []  # [no,word,tag]
for i in sentences[:12500]:
    for j in i:
        # print(j)
        words_list.append(j)
file[:] = words_list[:]
to_be_tested = sentences[12500:]
# print(to_be_tested)
# print("to_be_tested")
#####################################################################

for i in range(len(file)):  # setting appropriate data into map1 and list1
    temp = file[i].split('\t')
    if (len(temp) > 1):
        temp1.append(temp)
        if (list1.count(temp[2]) < 1):
            map1[temp[2]] = 1
            list1.append(temp[2])
        else:
            map1[temp[2]] += 1
# map1['UNK']=0
print(map1)
print(map1)
# print(list1)
print(len(map1))
sum = 0

# #transition matrix
#
# dict_transition = defaultdict(dict)  # transition probabilities are stored in this dictionary
# for i in list1:  # Initializing the values to zero
#     for j in list1:
#         dict_transition[i][j] = 0
# # print(dict_transition)
#
# tags = []  # contains all the tag pairs
# for i in range(len(list1)):  # making all possible tag pairs
#     for j in range(len(list1)):
#         temp = []
#         temp.append(list1[i])
#         temp.append(list1[j])
#         tags.append(temp)
# # print(tags)
#
# count1 = []
# for i in range(len(tags)):  # computing transition probability
#     count = 0
#     print(tags[i][0])
#     for j in range(len(temp1) - 1):
#         if (tags[i][0] == temp1[j][2] and tags[i][1] == temp1[j + 1][2]):
#             count += 1
#     # print(tags[i][0]+" "+tags[i][1]+" "+str(count))
#     # count1.append(count)
#     count = (count + 1) / (map1[tags[i][0]] + len(list1))  # laplace smoothing
#     #dict_transition[tags[i][0]][tags[i][1]] = math.log(count)
# print(dict_transition)
##########################################################
# observation matrix

# observation matrix (edited)

dict_words = defaultdict(dict)  # contains all the words and its respective counts

words = []  # contains list of all unique words
for i in range(len(temp1)):  # setting up words list and its corresponding count in a map too
    if (dict_words.get(temp1[i][1])):
        dict_words[temp1[i][1]] += 1
    else:
        dict_words[temp1[i][1]] = 1
        words.append(temp1[i][1])
print("words")
print(len(words))

# dealing with unknowns

single_count = 0  # tells us number of words that occured only once in the corpus
for i in dict_words.copy():
    # print(dict_words[i])
    if (dict_words[i] == 1):
        single_count += 1
        # print(i)
        dict_words.pop(i)
        words.remove(i);  # removing the words from the list whic are of frequency 1
        for j in temp1:  # replacing the words in the temp1 with 1 frequency to unknown
            if (j[1] == i):
                j[1] = 'unknown'

dict_words['unknown'] = single_count;
print(dict_words)
# print(len(dict_words))

words.append('unknown')  # adding unknown word into the words list.
print("With Unknown, No of words:")
print(len(words))


#############################################
words_tags = []  # contains all the words tags combination
dict_observation = defaultdict(dict)
for i in range(len(words)):
    for j in range(len(list1)):
        temp = []
        temp.append(words[i])
        temp.append(list1[j])
        words_tags.append(temp)
        dict_observation[words[i]][list1[j]]=0
#print(words_tags[0])
#print(len(words_tags))
#print(dict_observation)

for i in range(len(temp1)):
    dict_observation[temp1[i][1]][temp1[i][2]]+=1
#print(dict_observation)

##################################################
#another way to deal with the unknowns

##end of that
##################################################

dict_baseline=defaultdict(dict)
#dict_baseline[:]=dict_observation[:]
dict_baseline= copy.deepcopy(dict_observation)
for i in range(len(words)):
    for j in range(len(list1)):
        x=dict_observation[words[i]][list1[j]]/map1[list1[j]]
        if(x!=0):
            x=math.log(x)
        else:
            x=-999999
        dict_observation[words[i]][list1[j]] = x
print(dict_observation)

#print(dict_baseline)
#end of obervation matrix generation
###################################
##transition matrix

dict_transition = defaultdict(dict)  # transition probabilities are stored in this dictionary
for i in list1:  # Initializing the values to zero
    for j in list1:
        dict_transition[i][j] = 0
# print(dict_transition)

tags = []  # contains all the tag pairs
for i in range(len(list1)):  # making all possible tag pairs
    for j in range(len(list1)):
        temp = []
        temp.append(list1[i])
        temp.append(list1[j])
        tags.append(temp)
#print(tags)
#print(dict_transition)
for i in range(len(temp1)-1):
    #print(temp1[i+1])
    dict_transition[temp1[i+1][2]][temp1[i][2]]+=1
#print(dict_transition)

list_tags=list(map1.keys())
for i in range(len(list_tags)):
    for j in range(len(list_tags)):
        x=((dict_transition[list_tags[i]][list_tags[j]])+1)/(map1[list_tags[j]]+len(map1))
        x=math.log(x)
        dict_transition[list_tags[i]][list_tags[j]]=x
print("tra")
print(dict_transition)

###End of transition prob calculation
####################################################

# Initial probability
initial_prob = defaultdict(dict)
for i in range(len(list1)):
    initial_prob[list1[i]] = dict_transition[list1[i]]['.']
# print("Initial Probability")
#print(initial_prob)

# Final probability
final_prob = defaultdict(dict)
for i in range(len(list1)):
    final_prob[list1[i]] = dict_transition['.'][list1[i]]
#print(final_prob)

#####################################################

def viterbi_algo(observation, transition, initial, final, sequence, tags):
    # print(observation)
    # print(transition)
    # print(initial)
    # print(seq)

    # dealing with unknown words#################
    seq = []
    # print("sequence")
    # print(sequence)
    # print(sequence[0]+","+sequence[1])
    # print(x)
    # for i in range(len(sequence)):
    # print(i)
    # print(len(sequence[i]))
    # if(len(sequence[i])>1):
    #     for j in sequence[i]:
    #         seq.append(j)
    #print(sequence)
    for i in sequence:
        i = str(i)
        x = i.split('\t')
        # print(x)
        # print(x[1])
        seq.append(x[1])

    seq = seq[:len(seq) - 1]

    seq2 = []
    seq2[:] = seq[:]
    #print("seq")
    #print(seq)
    for i in range(len(seq)):
        if (seq[i] not in words):
            #print(seq[i])
            seq[i]='unknown'

    length = len(seq)
    #print(words)
    ############################################


    ########

    vit = defaultdict(dict)
    path = defaultdict(dict)

    # presetting
    for i in range(length):
        for j in range(len(tags)):
            vit[tags[j]][seq[i]] = 0
    # print(vit)
    # print('Hi' in vit['A'])
    # Initial column
    for i in range(1):
        for j in range(len(tags)):
            # print(tags[j])
            # print(seq[i])
            # print()
            vit[tags[j]][seq[i]] = initial[tags[j]] + observation[seq[i]][tags[j]]
            path[tags[j]][seq[i]] = 0

    #print(vit)
    #print("Hi")
    #print(path)
    # Remaining
    for i in range(1, length):
        for j in range(len(tags)):
            x = -999999
            highest_tag = ''
            for k in range(len(tags)):
               # print("vit[tags[j]][seq[i - 1]]:"+str(tags[j])+" "+str(seq[i - 1])+" "+str(vit[tags[j]][seq[i - 1]]))
                #print(vit[tags[j]][seq[i-1]])
                temp = vit[tags[k]][seq[i - 1]] + transition[tags[j]][tags[k]]
                #print(temp)
                #print("Temp:"+str(temp))
                if (temp > x):
                    highest_tag = tags[k]
                    x = temp
            vit[tags[j]][seq[i]] = x + observation[seq[i]][tags[j]]
            # print(tags[j])
            path[tags[j]][seq[i]] = highest_tag
        #print("highest tag")
        #print(highest_tag)
        #print(seq[i])

            # print(path)
    #print(vit)
    # print(len(vit))
    #print(path)

    # Termination
    max = -9999999
    end_tag = ''
    for i in range(len(vit)):
        temp = vit[tags[i]][seq[len(seq) - 1]]
        if (temp > max):
            max = temp
            end_tag = tags[i]
    max = max + final[end_tag]
    #print(max)
    #print(end_tag)

    tag_sequence=[]
    tag_sequence.append(end_tag)
    for i in range(len(seq)-1,-1,-1):
        tag_sequence.append(path[tag_sequence[len(tag_sequence)-1]][seq[i]])
    #print(tag_sequence)
    tag_sequence=tag_sequence[:len(tag_sequence)-1]
    tag_sequence.reverse()
    #print(tag_sequence)
    return tag_sequence
tags_path=[]
for i in range(len(to_be_tested)):
    path=viterbi_algo(dict_observation,dict_transition,initial_prob,final_prob,to_be_tested[i],list_tags)
    tags_path.append(path)
#viterbi_algo(dict_observation,dict_transition,initial_prob,final_prob,to_be_tested[50],list_tags)
print(tags_path)

tags_full=[]
for i in tags_path:
    for j in i:
        tags_full.append(j)
print(tags_full)
print(len(tags_full))
###############################################################
given_output_seq=[]
for i in range(len(to_be_tested)):
    for j in range(len(to_be_tested[i])):
        str1=str(to_be_tested[i][j])
        arr=str1.split('\t')
        #print(arr[2])
        if(arr[2]!='.'):
            given_output_seq.append(arr[2])
print(given_output_seq)
print(len(given_output_seq))
## def confusion_matrix():
count_match=0;
for i in range(len(given_output_seq)):
    if(tags_full[i]==given_output_seq[i]):
        count_match+=1
accuracy=count_match/len(given_output_seq)
print(accuracy)

#########################################
test_file=open("assgn2-test-set.txt")
test=test_file.read()
test_data=test.split("\n")
print(test_data)
#print(test)

test_sentences=[]
temp_sent = []  # temporary sentences # Basically the below for loop writes the sentences into an array(of sentences)
for i in test_data:
    if (len(i) > 1):
        temp_sent.append(i);
    else:
        test_sentences.append(temp_sent)
        temp_sent = []
print(test_sentences)
print(len(test_sentences))

test_path=[]
for i in range(len(test_sentences)):
    path = viterbi_algo(dict_observation, dict_transition, initial_prob, final_prob, test_sentences[i], list_tags)
    test_path.append(path)
print(test_path)

############################################
###############Writing into the file
for i in range(len(test_path)):  #appending the tag to the test data
    for j in range(len(test_path[i])):
        test_sentences[i][j]+='\t'+test_path[i][j]
print(test_sentences)

for i in range(len(test_sentences)):
    test_sentences[i][len(test_sentences[i])-1]+='\t.'
print(test_sentences)

f=open('output.txt','a')
f.truncate(0)
for i in range(len(test_sentences)):
    for j in range(len(test_sentences[i])):
        f.write(test_sentences[i][j]+'\n')
    f.write('\n')
f.close()


#########################################################################
def baseline(observation,to_be_tested):
    output=defaultdict(dict)
    for i in observation:
        min_tag=''
        min=-999999
        #print(i)
        #print(observation[i])
        for j in observation[i]:
            if observation[i][j] > min:
                min=observation[i][j]
                min_tag=j
        output[i]=min_tag
    print("Output")
    print(output)
    demo=[]
    for i in to_be_tested:
        for j in i:
            t = []
            temp = str(j)
            arr = temp.split('\t')
            t.append(arr[1])
            t.append(arr[2])
            demo.append(t)

    print(demo)
    count=0
    for i in range(len(demo)):
        if(output[demo[i][0]]==demo[i][1]):
           count+=1
    print("Baseline Accuracy "+str(count/len(demo)))
    print("Viterbi Accuracy "+str(accuracy))

baseline(dict_observation,to_be_tested)



