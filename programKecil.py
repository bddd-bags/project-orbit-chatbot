import re
import stringMatchingBM
import stringMatchingKMP

def parseQuery(query, kataPenting, keywordLain):
    parsedResult = []
    datePattern = re.compile(r'\d{2}.\d{2}.\d{4}')
    tempParse = datePattern.findall(query)

    for date in tempParse:
        parsedResult.append(date)

    for kata in kataPenting:
        kataPattern = re.compile(r'{}'.format(kata))
        tempParse = kataPattern.findall(query)
        for hasilKata in tempParse:
            parsedResult.append(hasilKata)

    for kata in keywordLain:
        kataPattern = re.compile(r'{}'.format(kata))
        tempParse = kataPattern.findall(query)
        for hasilKata in tempParse:
            parsedResult.append(hasilKata)

    return parsedResult

kataPenting = ["Kuis", "Ujian", "Tucil", "Tubes", "Praktikum"]
keywordLain = ["Deadline","Tampilkan","Kapan"]
query = input("Masukkan kalimat perintah: ")

print(parseQuery(query, kataPenting, keywordLain))
    
    
