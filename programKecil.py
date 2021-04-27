import re
import stringMatchingBM as bm
import stringMatchingKMP as kmp
import levenshteinDistance as ld

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

def commandValidation(query):
    command3 = ['Deadline']
    command4 = ['Task']
    command5 = ['Selesai'] #irisan sama command 4

    #variable pembantu
    irisan45 = False

    for command in command3:
        if command in query['validCommand']:
            #nampilin tugas
            print("Bot akan menampilkan deadline suatu tugas")
            return

    for command in command4:
        if command in query['validCommand']:
            #solusi sementara
            for command in command5:
                if command in query['additionalCommand']:
                    irisan45 = True
                    break
            if not irisan45:
                #Perbaharui deadline task
                #Validasi dulu kalau tasknya ada
                print("Bot akan memperbaharui deadline task sesuai ID")
                return
    if irisan45:
        #Perbaharui task, tandai sudah selesai
        #tambahin validasi kalau ada input tanggal
        #Validasi tasknya ada
        print("Bot akan menandai suatu task X sudah selesai")

def extractTask(query, validTask, stringMatching):
    task = {"id": "",
            "matkul":"",
            "jenis":"",
            "topik":"",
            "deadline":"",
            "status":""}
    # kodeMatkulPattern = re.compile(r'[a-zA-Z]{2}\d{4}')

    #Referensi regex buat ambil consecutive capitalized word: https://stackoverflow.com/questions/31570699/regex-to-get-consecutive-capitalized-words-with-one-or-more-words-doesnt-work
    #matkulPattern = re.compile(r'((?:[Mm]atkul|[Mm]ata [Kk]uliah)|[a-zA-Z]{2}\d{4})\s?([A-Za-z\s]*)?\s?([Tt]opik)\s(\b(?:[A-Z][a-z]*\b\s*)+)')
    matkulPattern = re.compile(r'\b(?:[A-Z][a-z]*\b\s*\d?)+')
    datePattern = re.compile(r'(\d{2}.\d{2}.\d{4}|\d{2}.(?:[Jj]anuari|[Ff]ebruari|[Mm]aret|[Aa]pril|[Mm]ei|[Jj]uni|[Jj]uli|[Aa]gustus|[Ss]eptember|[Oo]ktober|[Nn]ovember|[Dd]esember).\d{4})')
    topikPattern = re.compile(r'\b(?:[A-Z][a-z]*\b\s*\d)+')
    


    #Add task from query
    
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
            task["matkul"] = query[index+len(ejaMatkul)+1:index2]

        #Pake metode regex
        else:
            tempData = matkulPattern.findall(query[index+len(ejaMatkul)+1:])
            if (tempData):
                task["matkul"] = " ".join(tempData).strip()

    #Add topik
    if(index2 != -1):
        tempData = matkulPattern.findall(query[index2+len("topik")+1:])
        if (tempData):
            task["topik"] = " ".join(tempData).strip()


    #Add tanggal (deadline)
    #KAYANYA PERLU ADA VALIDASI LAGI, MUNGKIN JUGA ENGGAK. 
    tempData = datePattern.findall(query)
    if (tempData):
        if (len(tempData[0]) == 10):
            task["deadline"] = tempData[0].strip()
        else:
            task["deadline"] = convertDateFormat(tempData[0]).strip()

    
    #Add jenis task
    #yang di sini mungkin perlu dikasih validasi kalau tasknya kebanyakan
    for macamTask in validTask:
        if (stringMatching(query,macamTask)+1):
            task["jenis"] = macamTask
            break
    
    #Ini bisi ga perlu sih

    #Add status to unfinished
    task["status"] = "0"

    return task

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




jenisTask = ["Tubes","Tucil","Praktikum","Ujian","Kuis"]
commandTest = input("Masukkan perintah: ")
test = extractTask(commandTest,jenisTask, bm.stringMatching)
print(test)

#END OF TEST MAIN PROGRAM