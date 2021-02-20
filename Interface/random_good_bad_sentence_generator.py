import random
import re
import sqlite3
from bottle import get, post, request, route, run
import datetime


conn = sqlite3.connect('630_database.sqlite')
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY, Name STRING, Password STRING, DateLastLogin DATETIME)')
conn.commit()
cur.execute('CREATE TABLE IF NOT EXISTS Scores (id INTEGER PRIMARY KEY, UserID INTEGER, QuestionTuple STRING, PassFail BOOLEAN, Attempts INTEGER)')
conn.commit()
cur.execute('CREATE TABLE IF NOT EXISTS Attempts (id INTEGER PRIMARY KEY, ScoreID INTEGER, AttemptNo INTEGER, AttemptTime INTEGER)')
conn.commit()

def rand_sentence_generator():
    there = 'There'

    there_verbs = {'present':{'singular':['is'],
                              'plural':['are']},
                   'past':{'singular':['was'],
                           'plural':['were']},
                    'future':{'singular':['will be'],
                              'plural':['will be']}
                   }

    determiners = {'singular':['a','one'],
                   'plural':['a lot of','a ton of','few','a few','many','some','lots of'],
                   'uncountable':['little']
                   }

    subjects = {'person':{'singular':['person','teacher','professor','student','parent','boss', 'janitor', 'secretary'],
                          'plural':['people','teachers','professors','students','parents','bosses', 'janitors','secretaries']},
                'animate':{'singular':['dog','cat','gerbil','fish','squirrel'],
                           'plural':['dogs','cats','gerbils','fish','squirrels']},
                'inanimate':{'singular':['book','pencil','desk','chair','folder','map','computer'],
                             'plural':['books','pencils','desks','chairs','folders','maps','computers']}
                }

    subject_type_pronouns = {'person':{'singular':['He','She'],
                                       'plural':['They']},
                             'animate':{'singular':['It'],
                                       'plural':['They']},
                             'inanimate':{'singular':['It'],
                                       'plural':['They']}
                             }

    relativizers = {'person':['who'],'animate':['that','which'],'inanimate':['that','which']}

    rel_verbs = {'present':{'singular':{'person':['lives','sits','works','plays','teaches','learns','lies'],
                                    'animate':['lives','sits','works','plays','teaches','learns','lies'],
                                    'inanimate':['lies']},
                            'plural':{'person':['live','sit','work','play','teach','learn','lie'],
                                  'animate':['live','sit','work','play','teach','learn','lie'],
                                  'inanimate':['lie']}},
                'past':{'singular':{'person':['lived','sat','worked','played','taught','learned','lied'],
                                 'animate':['lived','sat','worked','played','taught','learned','lied'],
                                 'inanimate':['lied']},
                        'plural':{'person':['lived','sat','worked','played','taught','learned','lied'],
                                  'animate':['lived','sat','worked','played','taught','learned','lied'],
                                  'inanimate':['lied']}},
                'future':{'singular':{'person':['will live','will sit','will work','will play','will teach','will learn','will lie'],
                                   'animate':['will live','will sit','will work','will play','will teach','will learn','will lie'],
                                  'inanimate':['will lie']},
                          'plural':{'person':['will live','will sit','will work','will play','will teach','will learn','will lie'],
                                 'animate':['will live','will sit','will work','will play','will teach','will learn','will lie'],
                                  'inanimate':['will lie']}}
             }

    logical_pronoun_verb = {'present': {'singular': {'person': ['live', 'sit', 'work', 'play', 'teach', 'learn', 'lie'],
                                                      'animate': ['lives', 'sits', 'works', 'plays', 'teaches', 'learns', 'lies'],
                                                      'inanimate': ['lies']},
                                         'plural': {'person': ['live', 'sit', 'work', 'play', 'teach', 'learn', 'lie'],
                                                    'animate': ['live', 'sit', 'work', 'play', 'teach', 'learn', 'lie'],
                                                    'inanimate': ['lie']}},
                             'past': {'singular': {'person': ['lived', 'sat', 'worked', 'played', 'taught', 'learned', 'lied'],
                                                   'animate': ['lived', 'sat', 'worked', 'played', 'taught', 'learned', 'lied'],
                                                   'inanimate': ['lied']},
                                      'plural': {'person': ['lived', 'sat', 'worked', 'played', 'taught', 'learned', 'lied'],
                                                 'animate': ['lived', 'sat', 'worked', 'played', 'taught', 'learned', 'lied'],
                                                 'inanimate': ['lied']}},
                             'future': {'singular': {'person': ['will live', 'will sit', 'will work', 'will play', 'will teach', 'will learn','will lie'],
                                                     'animate': ['will live', 'will sit', 'will work', 'will play', 'will teach', 'will learn','will lie'],
                                                     'inanimate': ['will lie']},
                                        'plural': {'person': ['will live', 'will sit', 'will work', 'will play', 'will teach',
                                                              'will learn', 'will lie'],
                                                   'animate': ['will live', 'will sit', 'will work', 'will play', 'will teach',
                                                               'will learn', 'will lie'],
                                                   'inanimate': ['will lie']}}
                            }

    prepPhrase = ['at the school','in the school','at home','on the playground']

    sentence = ""
    rand_there_tense = random.choice(list(there_verbs.keys()))
    rand_there_number = random.choice(list(there_verbs[rand_there_tense].keys()))
    rand_there_verb = random.choice(list(there_verbs[rand_there_tense][rand_there_number]))
    rand_determiner = random.choice(list(determiners[rand_there_number]))
    rand_subject_type = random.choice(list(subjects))
    rand_subject = random.choice(list(subjects[rand_subject_type][rand_there_number]))
    my_logical_pronoun = random.choice(list(subject_type_pronouns[rand_subject_type][rand_there_number]))
    rand_relativizer = random.choice(list(relativizers[rand_subject_type]))
    rand_rel_verb = random.choice(list(rel_verbs[rand_there_tense][rand_there_number][rand_subject_type]))
    rand_logical_pronoun_verb = random.choice(list(logical_pronoun_verb[rand_there_tense][rand_there_number][rand_subject_type]))
    rand_prepPhrase = random.choice(prepPhrase)

    #print(rand_logical_pronoun_verb)
    #print(rand_rel_verb)
    #print(rand_relativizer)
    #print(my_logical_pronoun)
    #print(rand_subject_type)
    #print(rand_subject)
    #print(rand_determiner)
    #print(rand_there_verb)
    #print(rand_there_number)
    #print(rand_there_tense)


    good_sentence = sentence + there+" "+rand_there_verb+" "+rand_determiner+" "+rand_subject+" "+rand_relativizer+" "+rand_rel_verb+" "+rand_prepPhrase+"."
    multiple_sentence = sentence + there+" "+rand_there_verb+" "+rand_determiner+" "+rand_subject+". "+my_logical_pronoun+" "+rand_rel_verb+" "+rand_prepPhrase+"."
    bad_sentence = sentence + there + " " + rand_there_verb + " " + rand_determiner + " " + rand_subject + " " + rand_rel_verb + " " + rand_prepPhrase + "."

    return(multiple_sentence, good_sentence,bad_sentence,rand_relativizer)


@route('/')
@get('/login')
def loginPage():
    return '''
    <form action="/login" method="post">
        Name: <input name="name" type="text" /><br>
        Password: <input name="password" type="password" /><br>
        <input value="Submit" type="submit" />
    </form>
    '''

@post('/login')
def checkLogin():
    name = request.forms.get('name')
    password = request.forms.get('password')
    datelastlogin = datetime.datetime.now()

    names_lst = returnListUserNames()
    return(returnListUserNames())

    if name in names_lst:
        interact()
    else:
        insertUser(name, userID, password, datelastlogin)
        interact()
run()


def insertUser(name, password, datelastlogin):
    cur.execute('''INSERT INTO Users VALUES (:name, :password, :datelastlogin)''', {'Name': name, 'Password': password, 'DateLastLogin': datelastlogin})
    conn.commit()
    return(cur.lastrowid)

# call when?
def insertScores(userID, questionTuple, passFail, attempts):
    cur.execute('''INSERT INTO Scores VALUES (:UserID, :QuestionTuple, :PassFail, :Attempts)''', {'UserID':userID, 'QuestionTuple':questionTuple, 'PassFail':passFail, 'Attempts':attempts})
    conn.commit()
    return (cur.lastrowid)

# call after a scores table entry is made
def insertAttempt(scoreID, attemptNo, attemptTime):
    cur.execute('''INSERT INTO Attempts VALUES (:ScoreID, :AttemptNo, :AttemptTime)''', {'ScoreID':scoreID, 'AttemptNo':attemptNo, 'AttemptTime':attemptTime})
    conn.commit()
    return (cur.lastrowid)

def returnListUserNames():
    usernamesList_raw = cur.execute('SELECT Name FROM Users').fetchall()
    usernamesList = []
    for item in usernamesList_raw:
        usernamesList.append(item[0])
    conn.commit()
    return(usernamesList)

def returnListUserIDs():
    userIDList_raw = cur.execute('SELECT Name FROM Users').fetchall()
    userIDList = []
    for item in userIDList_raw:
        userIDList.append(item[0])
    conn.commit()
    return(userIDList_raw)

def getRandSentences():
    my_sentences = rand_sentence_generator()
    return(my_sentences)



@route('/')
@get('/interactpage')
def interactpage():
    my_sentences = getRandSentences()
    my_multiple_sentences = my_sentences[0]
    my_good_sentence = my_sentences[1]
    my_bad_sentence = my_sentences[2]
    my_relativizer = my_sentences[3]


    attempts = 0
    points = 0

    return '''
        <form action="/home" method="post">
            Instructions: Please combine the following sentences without using a conjunction.
            my_multiple_sentences
            Combined sentences: <input user_combo="user_combo" type="text" /><br>
            <input value="Submit" type="submit" />
        </form>
        '''


@route('/')
@get('/interactpage')
def interaction():
    for i in range(1,7):
        if user_combo == my_good_sentence:
            print("** Good job! **")
            points = points + 1
            attempts = attempts +1
            # fill out tables using functions above!
            break    # is this right??
        elif user_combo == my_bad_sentence:
            print("Please try again. Focus on the structure of the relative clause this time. ")
            user_combo = input("Type new answer here: ")
            if user_combo == my_good_sentence:
                print("** Great work! You fixed it! **")
                points = points + 1
                break
        else:
            if re.sub('which','that',user_combo) == my_good_sentence:
                print("** Good job! **")
                points = points + 1
                break
            elif re.sub('that','which',user_combo) == my_good_sentence:
                print("** Good job! **")
                points = points + 1
                break
            else:
                print("Please try again.")
            user_combo = input("Type new answer here: ")
            if user_combo == my_good_sentence:
                print("** Great work! You fixed it! **")
                points = points + 1
                break
    return(points)
run()


# incorporate this into the code? didn't have enough time to think it through last time
my_points = 0
while my_points < 2:
    points = interact()
    my_points = my_points+points
    print("\n")

print("Total points earned: ", my_points)



def main():
    interact()

if __name__ == "__main__":
    main()
