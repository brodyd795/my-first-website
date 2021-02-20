import random
import re
import sqlite3
from bottle import get, post, request, route, run, redirect, template, static_file
from datetime import datetime
import os
import string

conn = sqlite3.connect('630_database.sqlite')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Info (Username STRING, Points INTEGER, QuestionTuple STRING, PassFail STRING, Attempt STRING, Time INTEGER)')
conn.commit()

HEADER = "<html> <head> <title> Relatives </title> </head> <body style='background-color:white;'>" \
         "<div style='background-color:#c00'>" \
        "<h3>Learn how to deal with all your relatives!</h3><br><br>" \
        "</div> "

FOOTER = "<br><br>Our leader: <br><img src='static/photo.png'/></body> </html>"

username = ''
points = 0

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
    #rand_logical_pronoun_verb = random.choice(list(logical_pronoun_verb[rand_there_tense][rand_there_number][rand_subject_type]))
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


my_sentences = rand_sentence_generator()
my_multiple_sentences = my_sentences[0]
my_good_sentence = my_sentences[1]
my_relativizer = my_sentences[2]


@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./')
@route('/')
@get('/login')
def loginPage():
    return HEADER + '''
    <form action="login" method="post">
        Name: <input name="name" type="text" /><br>
        <input value="Submit" type="submit" />
    </form>
    ''' + FOOTER

@post('/login')
def checkLogin():
    global username
    global my_multiple_sentences
    global points
    time = str(datetime.now())
    all_usernames_raw = cur.execute('SELECT Username FROM Info').fetchall()
    all_usernames = []
    for item in all_usernames_raw:
        item = item[0]
        all_usernames.append(item)
    conn.commit()
    username = request.forms.get('name')
    if username in all_usernames:
        points = cur.execute("SELECT MAX(Points) FROM Info WHERE Username=" + "'" +username+"'").fetchone()[0]
        passfail = 'Begin'
        cur.execute('INSERT INTO Info (Username, Points, QuestionTuple, PassFail, Time) VALUES (?,?,?,?,?)',[username, points, my_multiple_sentences, passfail, time])
        conn.commit()
    else:
        points = 0
        passfail = 'Begin'
        cur.execute('INSERT INTO Info (Username, Points, QuestionTuple, PassFail, Time) VALUES (?,?,?,?,?)',[username, points, my_multiple_sentences, passfail, time])
        conn.commit()
    redirect('/interactpage')


@route('/interactpage')

def interactpage():
    feedback = ""
    return(HEADER+template('something.tpl', my_multiple_sentences=my_multiple_sentences, points=points, feedback=feedback)+FOOTER)


for i in range(5):
    @post('/newpage')
    def newpage():
        global points, my_multiple_sentences, my_good_sentence, my_relativizer
        time = str(datetime.now())
        user_combo_raw = request.forms.get('user_combo')
        user_combo = str(request.forms.get('user_combo')).lower().translate(str.maketrans('', '', string.punctuation)).strip()
        my_good_sentence_clean = str(my_good_sentence).lower().translate(str.maketrans('', '', string.punctuation))
        if user_combo == my_good_sentence_clean or re.sub('that', 'which',user_combo) == my_good_sentence_clean or re.sub('which','that',user_combo) == my_good_sentence_clean:
            points = points + 10
            passfail = 'True'
            feedback = ""
            cur.execute('INSERT INTO Info (Username, Points, QuestionTuple, PassFail, Attempt, Time) VALUES (?,?,?,?,?,?)',[username, points, my_multiple_sentences, passfail, user_combo, time])
            conn.commit()
            return HEADER + template('correctTemplate.tpl', points=points, user_combo=user_combo_raw) + FOOTER
        elif my_relativizer in user_combo:
            feedback = "It looks like you used the correct relative pronoun. Are you sure you typed the sentence correctly?"
            return HEADER + template('something.tpl', my_multiple_sentences=my_multiple_sentences, points=points,user_combo=user_combo_raw, feedback=feedback) + FOOTER








@post('/newpage')

def newpage():
    global points, my_multiple_sentences, my_good_sentence, my_relativizer

    time = str(datetime.now())
    user_combo_raw = request.forms.get('user_combo')
    user_combo = str(request.forms.get('user_combo')).lower().translate(str.maketrans('','',string.punctuation)).strip()
    my_good_sentence_clean = str(my_good_sentence).lower().translate(str.maketrans('','',string.punctuation))

    if user_combo == my_good_sentence_clean or re.sub('that','which',user_combo) == my_good_sentence_clean or re.sub('which','that',user_combo) == my_good_sentence_clean:
        points = points + 10
        passfail = 'True'
        cur.execute('INSERT INTO Info (Username, Points, QuestionTuple, PassFail, Attempt, Time) VALUES (?,?,?,?,?,?)', [username, points, my_multiple_sentences, passfail, user_combo, time])
        conn.commit()
        return HEADER + template('correctTemplate.tpl', points=points, user_combo=user_combo_raw) + FOOTER
    # elif re.sub('that'|'which','who',)

    elif my_relativizer in user_combo:
        feedback = "It looks like you used the correct relative pronoun. Are you sure you typed the sentence correctly?"
        return HEADER + template('something2.tpl', my_multiple_sentences=my_multiple_sentences, points=points, user_combo=user_combo_raw, feedback=feedback) + FOOTER
    else:
        passfail = 'InProgress'
        cur.execute('INSERT INTO Info (Username, Points, QuestionTuple, PassFail, Attempt, Time) VALUES (?,?,?,?,?,?)', [username, points, my_multiple_sentences, passfail, user_combo, time])
        conn.commit()
        return feedback1(user_combo_raw)


def feedback1(user_combo_raw):
    return HEADER + template('something2.tpl', my_multiple_sentences=my_multiple_sentences, points=points, user_combo=user_combo_raw) + FOOTER

@post('/newpage2')
def newpage2():
    global points
    global my_multiple_sentences
    time = str(datetime.now())
    user_combo_raw = request.forms.get('user_combo')
    user_combo = str(request.forms.get('user_combo')).lower().translate(str.maketrans('','',string.punctuation)).strip()
    if user_combo == str(my_good_sentence).lower().translate(str.maketrans('','',string.punctuation)) or re.sub('that','which',user_combo) == str(my_good_sentence).lower().translate(str.maketrans('','',string.punctuation)) or re.sub('which','that',user_combo) == str(my_good_sentence).lower().translate(str.maketrans('','',string.punctuation)):
        points = points + 10
        passfail = 'True'
        cur.execute('INSERT INTO Info (Username, Points, QuestionTuple, PassFail, Attempt, Time) VALUES (?,?,?,?,?,?)', [username, points, my_multiple_sentences, passfail, user_combo, time])
        conn.commit()
        return HEADER + template('correctTemplate.tpl', points=points, user_combo=user_combo_raw) + FOOTER
    else:
        passfail = 'InProgress'
        cur.execute('INSERT INTO Info (Username, Points, QuestionTuple, PassFail, Attempt, Time) VALUES (?,?,?,?,?,?)', [username, points, my_multiple_sentences, passfail, user_combo, time])
        conn.commit()
        return feedback2(user_combo_raw)

def feedback2(user_combo_raw):
    return HEADER + template('something3.tpl', my_multiple_sentences=my_multiple_sentences, points=points, user_combo=user_combo_raw) + FOOTER

@post('/newpage3')
def newpage3():
    global points
    global my_multiple_sentences
    time = str(datetime.now())
    user_combo_raw = request.forms.get('user_combo')
    user_combo = str(request.forms.get('user_combo')).lower().translate(str.maketrans('','',string.punctuation)).strip()
    if user_combo == str(my_good_sentence).lower().translate(str.maketrans('','',string.punctuation)) or re.sub('that','which',user_combo) == str(my_good_sentence).lower().translate(str.maketrans('','',string.punctuation)) or re.sub('which','that',user_combo) == str(my_good_sentence).lower().translate(str.maketrans('','',string.punctuation)):
        points = points + 10
        passfail = 'True'
        cur.execute('INSERT INTO Info (Username, Points, QuestionTuple, PassFail, Attempt, Time) VALUES (?,?,?,?,?,?)', [username, points, my_multiple_sentences, passfail, user_combo, time])
        conn.commit()
        return HEADER + template('correctTemplate.tpl', points=points, user_combo=user_combo_raw) + FOOTER
    else:
        passfail = 'InProgress'
        cur.execute('INSERT INTO Info (Username, Points, QuestionTuple, PassFail, Attempt, Time) VALUES (?,?,?,?,?,?)', [username, points, my_multiple_sentences, passfail, user_combo, time])
        conn.commit()
        return feedback3(user_combo_raw)

def feedback3(user_combo_raw):
    return HEADER + template('something4.tpl', my_multiple_sentences=my_multiple_sentences, points=points, user_combo=user_combo_raw) + FOOTER

@post('/newpage4')
def newpage4():
    global points
    global my_multiple_sentences
    time = str(datetime.now())
    user_combo_raw = request.forms.get('user_combo')
    user_combo = str(request.forms.get('user_combo')).lower().translate(str.maketrans('','',string.punctuation)).strip()
    if user_combo == str(my_good_sentence).lower().translate(str.maketrans('','',string.punctuation)) or re.sub('that','which',user_combo) == str(my_good_sentence).lower().translate(str.maketrans('','',string.punctuation)) or re.sub('which','that',user_combo) == str(my_good_sentence).lower().translate(str.maketrans('','',string.punctuation)):
        points = points + 10
        passfail = 'True'
        cur.execute('INSERT INTO Info (Username, Points, QuestionTuple, PassFail, Attempt, Time) VALUES (?,?,?,?,?,?)', [username, points, my_multiple_sentences, passfail, user_combo, time])
        conn.commit()
        return HEADER + template('correctTemplate.tpl', points=points, user_combo=user_combo_raw) + FOOTER
    else:
        passfail = 'InProgress'
        print(my_good_sentence)
        cur.execute('INSERT INTO Info (Username, Points, QuestionTuple, PassFail, Attempt, Time) VALUES (?,?,?,?,?,?)', [username, points, my_multiple_sentences, passfail, user_combo, time])
        conn.commit()
        return feedback4(user_combo_raw)

def feedback4(user_combo_raw):
    return HEADER + template('something5.tpl', my_multiple_sentences=my_multiple_sentences, my_good_sentence=my_good_sentence, points=points, user_combo=user_combo_raw) + FOOTER

@post('/newpage5')
def newpage5():
    global points
    global my_multiple_sentences
    time = str(datetime.now())
    user_combo_raw = request.forms.get('user_combo')
    user_combo = str(request.forms.get('user_combo')).lower().translate(str.maketrans('','',string.punctuation)).strip()
    if user_combo == str(my_good_sentence).lower().translate(str.maketrans('','',string.punctuation)) or re.sub('that','which',user_combo) == str(my_good_sentence).lower().translate(str.maketrans('','',string.punctuation)) or re.sub('which','that',user_combo) == str(my_good_sentence).lower().translate(str.maketrans('','',string.punctuation)):
        points = points + 10
        passfail = 'True'
        cur.execute('INSERT INTO Info (Username, Points, QuestionTuple, PassFail, Attempt, Time) VALUES (?,?,?,?,?,?)', [username, points, my_multiple_sentences, passfail, user_combo, time])
        conn.commit()
        return HEADER + template('correctTemplate.tpl', points=points, user_combo=user_combo_raw) + FOOTER
    else:
        passfail = 'False'
        cur.execute('INSERT INTO Info (Username, Points, QuestionTuple, PassFail, Attempt, Time) VALUES (?,?,?,?,?,?)', [username, points, my_multiple_sentences, passfail, user_combo, time])
        conn.commit()
        return feedback5(user_combo_raw)

def feedback5(user_combo_raw):
    return HEADER + template('something5.tpl', my_multiple_sentences=my_multiple_sentences, my_good_sentence=my_good_sentence, points=points, user_combo=user_combo_raw) + FOOTER

@post('/redirectpage')
def redirectpage():
    global my_sentences
    my_sentences = rand_sentence_generator()
    global my_multiple_sentences
    my_multiple_sentences = my_sentences[0]
    global my_good_sentence
    my_good_sentence = my_sentences[1]
    redirect('/interactpage')



if __name__ == '__main__':
    run(host="127.0.0.1", port=8080, reloader=True)




# Old Stuff
"""
cur.execute('CREATE TABLE IF NOT EXISTS Scores (id INTEGER PRIMARY KEY AUTOINCREMENT, UserID INTEGER, QuestionTuple STRING, PassFail BOOLEAN, Attempts INTEGER)')
conn.commit()
cur.execute('CREATE TABLE IF NOT EXISTS Attempts (id INTEGER PRIMARY KEY AUTOINCREMENT, ScoreID INTEGER, AttemptNo INTEGER, AttemptTime INTEGER)')
conn.commit()

globalscore = {'id':None, 'userID':None, 'questiontuple':None, 'passfail':None, 'attempts':None}
globalattempt = {'id':None, 'scoreID':None, 'attemptNo':None, 'attemptTime':None}


def insertScore(userID, questionTuple, passFail, attempts):
   cur.execute('''INSERT INTO Scores VALUES (:UserID, :QuestionTuple, :PassFail, :Attempts)''', {'UserID':userID, 'QuestionTuple':questionTuple, 'PassFail':passFail, 'Attempts':attempts})
   conn.commit()
    return(cur.lastrowid)

def insertAttempt(scoreID, attemptno, attempttime):
   cur.execute('''INSERT INTO Attempts VALUES (:ScoreID, :AttemptNo, :AttemptTime)''', {'ScoreID':scoreID, 'AttemptNo':attemptno, 'AttemptTime':attempttime})
    conn.commit()
    return(cur.lastrowid)

def getScore():
    cur.execute("SELECT * FROM Scores WHERE id=?", (str(globalscore['id']),))
    myscore = cur.fetchall()
    return (myscore)

def getAttempt():
   cur.execute("SELECT * FROM Attempts WHERE id=?", (str(globalattempt['id']),))
    myattempt = cur.fetchall()
   return (myattempt)
"""
