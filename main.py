import os
import time
import json
import urllib

html_replace = { '&lt;' : '<' , '&gt;' : '>' , '&amp;' : '&' , '&quot;' : '\"' , "&apos;" : "'" , '\r' : '' }
languages    = { 'Python' : '.py' , 'C' : '.c', 'Java' : '.java' , 'C#' : '.cs' }

def initialise():

    global CF_handle,all_submissions,logs
    base_path = 'Codeforces'

    
    CF_handle = raw_input('Enter Your Codeforces Handle :\t')

    if not os.path.exists(base_path):
        os.mkdir(base_path)

    
    if not os.path.exists(base_path + '/' + CF_handle):
        os.mkdir(base_path + '/' + CF_handle)

    logs = open(base_path + '/' + "Logs.txt","w")
    logs.write('LOGS :\n\n')
    logs.write('\tHandle : ' +  CF_handle + '\n')
    


    user_status = urllib.urlopen('http://codeforces.com/api/user.status?handle=' + CF_handle + '&from=1&count=1234567').read()
    user_data   = json.loads(user_status)

   
    if user_data['status'] ==  u'OK' :
        all_submissions = user_data['result']

    else :
        print ('SomeThing Weird has Occured')
        exit(0)

    print 'Total Submissions : %d' %(len(all_submissions))
    logs.write( '\tTotal Submissions : %d\n\n' %(len(all_submissions)) )
    

    extract_codes(all_submissions)


                        
def extract_codes(submissions):

        JUGGAAD = '<pre class="prettyprint program-source" style="padding: 0.5em;">'
        
        previous_contest_id = -1
        for submission in submissions:
                if submission['verdict'] == u'OK' :

                        contest_id    = submission['contestId']
                        problem_index = submission['problem']['index']
                        problem_name  = submission['problem']['name']
                        submission_id = submission['id']
                        language      = submission['programmingLanguage']

                        if contest_id != previous_contest_id :
                                previous_contest_id = contest_id
                                logs.write('\t' + str(contest_id) + ' :\n')
                                
                        logs.write('\t\t' + str(submission_id) + '\t' + str(problem_index) + '\t' + str(problem_name) + '\t\t' +  language + '\n')

                        full_page  = urllib.urlopen('http://codeforces.com/contest/' + str(contest_id) + '/submission/' + str(submission_id) ).read()

                        code_start = full_page.find(JUGGAAD) + len(JUGGAAD)
                        code_end   = full_page.find('</pre>',code_start)

                        code_raw   = full_page[code_start : code_end ]
                        code       = html_handle(code_raw)
                        save_code(contest_id,problem_index,problem_name,code,extension(language))
                        
        logs.close()


def extension(language):

    if 'C++' in language :
        return '.cpp'
    for lang in languages :
        if lang in language:
            return languages[lang]
    return '.unknown'


def html_handle(code_raw):

    for raw_data in html_replace :
            code_raw = code_raw.replace(raw_data, html_replace[raw_data])
    
    return code_raw


def save_code(contest_id,problem_index,problem_name,code,problem_extension):

    base_path = 'Codeforces' + '/' + CF_handle + '/' + str(contest_id)

    if not os.path.exists(base_path):
        os.mkdir(base_path)


    file = open(base_path + '/' + problem_name + '(' + problem_index + ')' + problem_extension,'w')    
    file.write(code)
    file.close()


if __name__ == '__main__':
        initialise()
