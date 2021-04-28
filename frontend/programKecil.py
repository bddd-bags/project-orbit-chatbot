import re
import stringMatchingBM as bm
import stringMatchingKMP as kmp
import levenshteinDistance as ld
from flask_sqlalchemy import SQLAlchemy


def convertDateFormat(date):
    temp = date.split()

    #Convert to lowercase if not already
    temp[1] = temp[1].lower()
    if (len(temp)> 1):
        if temp[1] == "januari":
            temp[1] = "01"
        if temp[1] == "februari":
            temp[1] = "02"
        if temp[1] == "maret":
            temp[1] = "03"
        if temp[1] == "april":
            temp[1] = "04"
        if temp[1] == "mei":
            temp[1] = "05"
        if temp[1] == "juni":
            temp[1] = "06"
        if temp[1] == "juli":
            temp[1] = "07"
        if temp[1] == "agustus":
            temp[1] = "08"
        if temp[1] == "september":
            temp[1] = "09"
        if temp[1] == "oktober":
            temp[1] = "10"
        if temp[1] == "november":
            temp[1] = "11"
        if temp[1] == "desember":
            temp[1] = "12"
    
    fixedDate = "/".join(temp)

    return fixedDate

def parseQuery(query, kataPenting, validCommand, additionalCommand,stringMatching):
    result = {"kataPenting": [],
                "validCommand": [],
                "additionalCommand": [],
                "task": [],
                "tanggal":[]}

    for kata in kataPenting:
        if(stringMatching(query,kata)+1):
            result["kataPenting"].append(kata)
    
    for keyword in validCommand:
        if(stringMatching(query,keyword)+1):
            result["validCommand"].append(keyword)
    
    for keyword in additionalCommand:
        if(stringMatching(query,keyword)+1):
            result["additionalCommand"].append(keyword)
    
    datePattern = re.compile(r'\d{2}.\d{2}.\d{4}')
    tempParse = datePattern.findall(query)

    for date in tempParse:
        result["tanggal"].append(date)
    
    return result


def commandRecognition(query, commandDB):
    validCommand = [0 for i in range(len(commandDB))]

    for keyword in query['validCommand']: #Kayanya ini perlu dibikin lebih dinamik
        for i, command in enumerate(commandDB):
            if keyword == command:
                validCommand[i] += 1
    if sum(validCommand) == 1:
        return True
    else:
        return False

# def commandValidation(query):
#     command3 = ['Deadline']
#     command4 = ['Task']
#     command5 = ['Selesai'] #irisan sama command 4

#     #variable pembantu
#     irisan45 = False

#     for command in command3:
#         if command in query['validCommand']:
#             #nampilin tugas
#             print("Bot akan menampilkan deadline suatu tugas")
#             return

#     for command in command4:
#         if command in query['validCommand']:
#             #solusi sementara
#             for command in command5:
#                 if command in query['additionalCommand']:
#                     irisan45 = True
#                     break
#             if not irisan45:
#                 #Perbaharui deadline task
#                 #Validasi dulu kalau tasknya ada
#                 print("Bot akan memperbaharui deadline task sesuai ID")
#                 return
#     if irisan45:
#         #Perbaharui task, tandai sudah selesai
#         #tambahin validasi kalau ada input tanggal
#         #Validasi tasknya ada
#         print("Bot akan menandai suatu task X sudah selesai")

def parseCommand(query,command, stringMatching):
    parsed = [[] for i in range(len(command))]

    for count, availableCommand in enumerate(command):
        if (stringMatching(query,availableCommand)+1):
            parsed[count].append(availableCommand)
    
    return parsed

def extractTask(query, deadlineTask,normalTask, stringMatching):
    task = {"id": [],
            "matkul":[],
            "jenis":[],
            "topik":[],
            "deadline":[],
            "status":[]}
    # kodeMatkulPattern = re.compile(r'[a-zA-Z]{2}\d{4}')

    #Referensi regex buat ambil consecutive capitalized word: https://stackoverflow.com/questions/31570699/regex-to-get-consecutive-capitalized-words-with-one-or-more-words-doesnt-work
    #matkulPattern = re.compile(r'((?:[Mm]atkul|[Mm]ata [Kk]uliah)|[a-zA-Z]{2}\d{4})\s?([A-Za-z\s]*)?\s?([Tt]opik)\s(\b(?:[A-Z][a-z]*\b\s*)+)')
    idPattern = re.compile(r'[Tt]ask\s\d*')
    matkulPattern = re.compile(r'(\b(?:[A-Z][a-z]*\b\s*\d?)+|[A-Z]{2}\d{4})')
    datePattern = re.compile(r'(\d{2}.\d{2}.\d{4}|\d{2}.(?:[Jj]anuari|[Ff]ebruari|[Mm]aret|[Aa]pril|[Mm]ei|[Jj]uni|[Jj]uli|[Aa]gustus|[Ss]eptember|[Oo]ktober|[Nn]ovember|[Dd]esember).\d{4})')
    # topikPattern = re.compile(r'\b(?:[A-Z][a-z]*\b\s*\d)+')
    topikPattern = re.compile(r'(\b(?:[A-Z][a-z]*\b\s*\d?)+|[A-Z]{2}\d{4})')
    # topikPattern = re.compile(r'^topik\s')


    #Add task from query

    #Add ID

    tempData = idPattern.findall(query)
    if(tempData):
        for id in tempData:
            task["id"].append(id.split()[1])
    
    #Add matkul/kode matkul
    #ALGO LAMA/KAYANYA UDAH OBSOLETE
    # tempData = matkulPattern.findall(query)
    # print(tempData)
    # if (tempData):
    #     if (tempData[0][0][3].isdigit()):
    #         task["matkul"] = tempData[0][0].strip()
    #     else:
    #         task["matkul"] = tempData[0][1].strip()

    index = -1
    for cariMatkul in ["matkul", "mata kuliah"]:
        if (stringMatching(query,cariMatkul)+1):
            print("Masuk sini")
            ejaMatkul = cariMatkul
            index = stringMatching(query,cariMatkul)
    
    #Pake metode stringMatching
    index2 = stringMatching(query,"topik") #Ini kepake juga buat topik
    if(index != -1):
        if (index2 != -1):
            task["matkul"].append(query[index+len(ejaMatkul)+1:index2-1])

        #Pake metode regex
        else:
            tempData = matkulPattern.findall(query[index+len(ejaMatkul)+1:])
            if (tempData):
                task["matkul"].append(" ".join(tempData).strip())

    #Add topik
    if(index2 != -1):
        tempData = topikPattern.findall(query[index2+len("topik")+1:])
        if (tempData):
            task["topik"].append(" ".join(tempData).strip())


    #Add tanggal (deadline)
    #KAYANYA PERLU ADA VALIDASI LAGI, MUNGKIN JUGA ENGGAK. 
    tempData = datePattern.findall(query)
    if (tempData):
        for date in tempData:
            if (len(date) == 10):
                task["deadline"].append(date.strip())
            else:
                task["deadline"].append(convertDateFormat(date).strip())

    
    #Add jenis task
    #yang di sini mungkin perlu dikasih validasi kalau tasknya kebanyakan
    for macamTask in deadlineTask:
        if (stringMatching(query,macamTask)+1):
            task["jenis"].append(macamTask)
            #Add status to unfinished
            # task["status"].append("0")
    
    for macamTask in normalTask:
        if (stringMatching(query,macamTask)+1):
            task["jenis"].append(macamTask)
            #Add status to unfinished
            # task["status"].append("-1")
    
    #Ini bisi ga perlu sih

    

    return task

def extractNHariPekan(query):
    hariPekanPattern = re.compile(r'(\d*)\s([Hh]ari|[Mm]inggu)')
    result = []
    hasilPattern = hariPekanPattern.findall(query)

    if (hasilPattern):
        for N in hasilPattern[0]:
            if N.isdigit():
                result.append(int(N))
    return result

#TEST MAIN PROGRAM

# kataPenting = ["Kuis", "Ujian", "Tucil", "Tubes", "Praktikum"]
# commandDB = ["Deadline","Tampilkan","Kapan","Task"]
# additionalCommand = ["Selesai"]
# query = input("Masukkan kalimat perintah: ")
# parsedQuery = parseQuery(query, kataPenting, commandDB,additionalCommand, bm.stringMatching)

# if commandRecognition(parsedQuery,commandDB):
#     commandValidation(parsedQuery)
# else:
#     #masuk ke bagian rekomendasi
#     threshold = 0.25
#     reccomendation = ld.missWordRecc(query,commandDB,threshold)
#     if (reccomendation):
#         #Ini masih belum sih
#         print("Sepertinya kamu typo! Apakah maksud kamu "+ reccomendation[0]+"?")
#     else:
#         print("Perintah tidak dikenali")


#Input nama matkul harus diawali pake kata 'matkul'/'mata kuliah'
#Input nama topik harus diawali kata 'topik'
#Kalau dalam satu input ada nama matkul dan topik, inputnya harus berurutan matkul terus topik
#Input nama matkul(kecuali kalau inputnya kode matkul) sama topik matkul harus selalu diawali huruf kapital
#ex: Aku mau lihat deadline Matkul IF2211 topik Dynamic Programming




def isTaskInputComplete(task):
    return len(task["matkul"]) == len(task["jenis"]) and len(task["jenis"]) == len(task["topik"]) and len(task["topik"]) == len(task["deadline"]) and len(task["deadline"]) >= 1

def isTaskInputEmpty(task):
    return len(task["matkul"]) == len(task["jenis"]) and len(task["jenis"]) == len(task["topik"]) and len(task["topik"]) == len(task["deadline"]) and len(task["deadline"]) == 0

def isTaskOnlyX(task, taskX, attributeTask, stringMatching):
    if  len(task[taskX]) > 0:
        for taskAttribute in attributeTask:
            # print("ini string matchingnya", stringMatching(taskX,taskAttribute)+1)
            # print("ini string len tasknya", len(task[taskAttribute]))
            if stringMatching(taskX,taskAttribute) == -1 and len(task[taskAttribute]) != 0:
                if(taskAttribute != "deadline" and taskAttribute!= "jenis"):
                    # print("yang dicari tuh", taskX)
                    # print("task", taskAttribute,"ga kosong")
                    return -1
        return len(task[taskX])
    return -1



def commandToIndex(command,commandDB, stringMatching):
    for index, availableCommand in enumerate(commandDB):
        if stringMatching(command,availableCommand)+1:
            return index
    return -1

def isCommandEmpty(command):
    for availableCommand in command:
        if (len(availableCommand) != 0):
            return False
    return True

def isCommandOnlyX(userCommand, commandX, commandDB, stringMatching):
    commandIndex = commandToIndex(commandX, commandDB, stringMatching)
    if  (commandIndex+1):
        for count, availableCommand in enumerate(userCommand):
            if count == commandIndex and len(availableCommand)!= 0:
                return True
            elif len(availableCommand) != 0:
                return False
    return False

def isCommandOnlyXandY(userCommand, commandX,commandY, commandDB, stringMatching):
    commandIndex1 = commandToIndex(commandX, commandDB, stringMatching)
    commandIndex2 = commandToIndex(commandY, commandDB, stringMatching)
    if  (commandIndex1+1 and commandIndex2+1):
        # print("panjang command 1", len(userCommand[commandIndex1]))
        # print("panjang command 2", len(userCommand[commandIndex2]))
        if len(userCommand[commandIndex1]) != len(userCommand[commandIndex2]):
            return False
        if len(userCommand[commandIndex1]) == 0 or len(userCommand[commandIndex2]) == 0:
            return False
        if (len(userCommand[commandIndex1]) == len(userCommand[commandIndex2]) and len(userCommand[commandIndex1]) != 0):
            for count, availableCommand in enumerate(userCommand):
                if len(availableCommand)!= 0:
                    if availableCommand[0] != commandX and availableCommand[0] != commandY:
                        return False
    return True


def taskDBToString(taskDB):
    result = ""
    for num, task in enumerate(taskDB):
        result += str(num+1)+". "
        result += "(ID: " + str(task.id) +") "
        result += task.deadline + " - "
        result += task.matkul + " - "
        result += task.jenis + " - "
        result += task.topik + " - "#+ "BBBBBBBBBBBBBBBBBBBBBBBBB"
        result += "       "
    return result

def filterDBTask(taskDB, filter, keyWord):
    result = []
    if filter == "matkul":
        for task in (taskDB):
            if (task.matkul == keyWord):
                result.append(task)
    if filter == "jenis":
        for task in (taskDB):
            if (task.jenis == keyWord):
                result.append(task)
    return result


def commandValidation(mainCommand,additionalCommand,mainCommandList, additionalCommandList,task, attributeTask,nHariPekan, stringMatching, taskFromDB):
    print("Masuk validation")
    #case 1 (kayanya ini nanti taruh bawah sih kalau udah kelar)
    if ((isCommandEmpty(mainCommand) or isCommandOnlyX(mainCommand,"deadline",mainCommandList,stringMatching)) and isCommandEmpty(additionalCommand)):
        if(isTaskInputComplete(task)):
            output = "Case 1! Jalankan fungsi add task"
            return output
            #masih ngebug, sementara tanganin pake return
            #tambahin fungsi add task ke sini
        elif(isCommandOnlyX(mainCommand,"deadline",mainCommandList,stringMatching)):
            print("skip case 1")
        else:
            #tasknya kaga lengkap/invalid
            #tambahin pesan kesalahan di sini
            print("Maaf perintah kamu kurang tepat. Task kamu tidak lengkap!")
    #case 4 (ditaruh di sini karena suatu hal)
    if (isCommandOnlyXandY(mainCommand,"Deadline","Diundur",mainCommandList,stringMatching)):
        print("Case 4! Jalankan fungsi update deadline task!")

    #case 2
    elif(isCommandOnlyX(mainCommand,"deadline",mainCommandList,stringMatching)):
        #2.c harus di atas soalnya dia bisa digabung sama yang lain
        # print(isTaskOnlyX(task, "jenis", attributeTask,stringMatching))
        if (isTaskOnlyX(task, "jenis", attributeTask, stringMatching) != -1):
            print("Case 2.c! Jalankan fungsi tampilkan task dengan jenis tertentu!")
            return taskDBToString(filterDBTask(taskFromDB,"jenis",task["jenis"][0]))
        #2.a
        if isCommandEmpty(additionalCommand) and isTaskInputEmpty(task):
            print("Case 2.a! Jalankan fungsi menampilkan seluruh task!")
            return taskDBToString(taskFromDB)
        #2.b1
        elif (isCommandOnlyX(mainCommand,"deadline",mainCommandList,stringMatching) and isTaskOnlyX(task,"deadline",attributeTask, stringMatching) == 2):
            print("Case 2.b1! Jalankan fungsi menampilkan task di antara dua buah tanggal!")
        elif(isCommandOnlyX(mainCommand,"deadline",mainCommandList,stringMatching) and len(nHariPekan) == 1):
            #2.b2
            if(isCommandOnlyX(additionalCommand,"hari",additionalCommandList,stringMatching)):
                print("Case 2.b2! Jalankan fungsi menampilkan task N hari dari sekarang!")
            #2.b3
            if(isCommandOnlyX(additionalCommand,"minggu",additionalCommandList,stringMatching)):
                print("Case 2.b3! Jalankan fungsi menampilkan task N minggu dari sekarang!")
        #2.b4
        elif(isCommandOnlyX(additionalCommand,"hari ini",additionalCommandList,stringMatching)):
            print("Case 2.b4! Jalankan fungsi menampilkan task hari ini")
        
        #case 3
        #tambahin fungsi buat nyari ID sama validasi inputnya cm ada ID
        elif (isTaskOnlyX(task,"matkul",attributeTask,stringMatching)):
            # filterDBTask(taskFromDB,"matkul",task["matkul"][0])
            # return filterDBTask(taskFromDB,"matkul",task["matkul"][0])[0].tanggal
            print("Case 3! Jalankan fungsi search matkul by ID/Nama matkul")

        

        
        # elif
    
    #case 5
    elif(isCommandOnlyX(mainCommand,"selesai",mainCommandList,stringMatching)):
        print("Case 5! jalankan fungsi update task selesai")

    else:
        #perintah tidak dikenali
        print("Perintah kamu tidak dikenali!")
        return "waduh, botnya bingung bang. Coba ketik help deh!"
    return



def commandValidationTest(mainCommand,additionalCommand,mainCommandList, additionalCommandList,task, attributeTask,nHariPekan, stringMatching):
    print("Masuk validation")
    #case 1 (kayanya ini nanti taruh bawah sih kalau udah kelar)
    if ((isCommandEmpty(mainCommand) or isCommandOnlyX(mainCommand,"deadline",mainCommandList,stringMatching)) and isCommandEmpty(additionalCommand)):
        if(isTaskInputComplete(task)):
            output = "Case 1! Jalankan fungsi add task"
            return output
            #masih ngebug, sementara tanganin pake return
            #tambahin fungsi add task ke sini
        elif(isCommandOnlyX(mainCommand,"deadline",mainCommandList,stringMatching)):
            print("skip case 1")
        else:
            #tasknya kaga lengkap/invalid
            #tambahin pesan kesalahan di sini
            print("Maaf perintah kamu kurang tepat. Task kamu tidak lengkap!")
    #case 4 (ditaruh di sini karena suatu hal)
    if (isCommandOnlyXandY(mainCommand,"Deadline","Diundur",mainCommandList,stringMatching)):
        print("Case 4! Jalankan fungsi update deadline task!")

    #case 2
    elif(isCommandOnlyX(mainCommand,"deadline",mainCommandList,stringMatching)):
        #2.c harus di atas soalnya dia bisa digabung sama yang lain
        # print(isTaskOnlyX(task, "jenis", attributeTask,stringMatching))
        if (isTaskOnlyX(task, "jenis", attributeTask, stringMatching) != -1):
            print("Case 2.c! Jalankan fungsi tampilkan task dengan jenis tertentu!")
            # return taskDBToString(filterDBTask(taskFromDB,"jenis",task["jenis"][0]))
        #2.a
        if isCommandEmpty(additionalCommand) and isTaskInputEmpty(task):
            print("Case 2.a! Jalankan fungsi menampilkan seluruh task!")
            # return taskDBToString(taskFromDB)
        #2.b1
        elif (isCommandOnlyX(mainCommand,"deadline",mainCommandList,stringMatching) and isTaskOnlyX(task,"deadline",attributeTask, stringMatching) == 2):
            print("Case 2.b1! Jalankan fungsi menampilkan task di antara dua buah tanggal!")
        elif(isCommandOnlyX(mainCommand,"deadline",mainCommandList,stringMatching) and len(nHariPekan) == 1):
            #2.b2
            if(isCommandOnlyX(additionalCommand,"hari",additionalCommandList,stringMatching)):
                print("Case 2.b2! Jalankan fungsi menampilkan task N hari dari sekarang!")
            #2.b3
            if(isCommandOnlyX(additionalCommand,"minggu",additionalCommandList,stringMatching)):
                print("Case 2.b3! Jalankan fungsi menampilkan task N minggu dari sekarang!")
        #2.b4
        elif(isCommandOnlyX(additionalCommand,"hari ini",additionalCommandList,stringMatching)):
            print("Case 2.b4! Jalankan fungsi menampilkan task hari ini")
        
        #case 3
        #tambahin fungsi buat nyari ID sama validasi inputnya cm ada ID
        elif (isTaskOnlyX(task,"matkul",attributeTask,stringMatching)):
            # filterDBTask(taskFromDB,"matkul",task["matkul"][0])
            # return filterDBTask(taskFromDB,"matkul",task["matkul"][0])[0].tanggal
            print("Case 3! Jalankan fungsi search matkul by ID/Nama matkul")

        

        
        # elif
    
    #case 5
    elif(isCommandOnlyX(mainCommand,"selesai",mainCommandList,stringMatching)):
        print("Case 5! jalankan fungsi update task selesai")

    else:
        #perintah tidak dikenali
        print("Perintah kamu tidak dikenali!")
        return "waduh, botnya bingung bang. Coba ketik help deh!"
    return


jenisTaskDeadline = ["Tubes","Tucil"]
jenisTaskNormal = ["Praktikum","Ujian","Kuis"]
attributeTask = ["id","matkul","jenis","topik","deadline","status"]

mainCommandList = ["Deadline", "Diundur", "Selesai"]
additionalCommandList = ["Hari", "Minggu", "Hari Ini","Task"]



# query = input("Masukkan perintah: ")

#test case 1
# query = "bot, tolong ingetin kalau ada deadline tucil matkul IF2211 topik Pemrograman dikumpul 10 April 2020"


#test case 2a
# query = "aku mau tahu deadlineku!"

#test case 2b1
# query = "bot tolong tampilkan deadline dari tanggal 20 April 2020 sampai 22 April 2020!"

#test case 2b2
# query = "apa aja deadline 10 minggu dari sekarang?"

#test case 2b3
# query ="deadline 5 hari ke depan"

#test case 2b4
# query = "deadline hari ini"

# test case 2c
# query = "deadline tubes dari tanggall 20/04/2020 sampai tanggal 21/05/2020"
# query = "deadline tucil 5 hari ke depan"
# query = "deadline tubes 5 minggu ke depan"
# query = "deadline tucil hari ini"


# test case 3
# baru jalan kalau pake nama matkul. PR: tambahin kalau yang dimasukin ID task; eh udah jalan, ga tahu kenapa wkwkk
query = "kapan deadline matkul IF2211?"
# query = "kapan deadline task 10?"

#test case 4
# query = "deadline task 4 diundur jadi 20/04/2020"

#test case 5
# query = "task 5 selesai"

mainCommand = parseCommand(query,mainCommandList, bm.stringMatching)
additionalCommand = parseCommand(query,additionalCommandList, bm.stringMatching)
tasks = extractTask(query,jenisTaskDeadline,jenisTaskNormal,bm.stringMatching)
nHariPekan = extractNHariPekan(query)


print(isCommandOnlyX(mainCommand,"deadline", mainCommandList,bm.stringMatching))
print(isTaskOnlyX(tasks,"jenis",attributeTask,bm.stringMatching))

print("ini main command:", mainCommand)
print("ini additional command:", additionalCommand)
print("ini hasil ekstraksi N hari atau minggu:",nHariPekan)
print("ini task:",tasks)
print("Testing fungsi cocokin 2 command",isCommandOnlyXandY(mainCommand, "Deadline","Diundur", mainCommandList, bm.stringMatching))
commandValidationTest(mainCommand, additionalCommand,mainCommandList,additionalCommandList, tasks, attributeTask,nHariPekan, bm.stringMatching)





#END OF TEST MAIN PROGRAM