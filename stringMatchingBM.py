def buildLast(pattern):
    #Jumlah karakter ASCII ada 128
    last = [-1 for i in range(128)]
    for index, char in enumerate(pattern):
        # ord = fungsi buat dapetin ASCII dari suatu char
        last[ord(char)] = index
    return last

def stringMatchingBM(text, pattern):
    j = len(pattern)-1
    i = j
    n = len(text)
    m = len(pattern)
    lastO = buildLast(pattern)
    while (i < n):
        if (text[i] == pattern[j]):
            if (j == 0):
                #if found matching pattern
                return i
            #looking-glass
            i -= 1
            j -= 1
        else:
            #Geser i sesuai kasus (1, 2, atau 3)
            i = i + m - min(j, lastO[ord(text[i])]+1)

            #Balikin lagi j ke indeks akhir pattern
            j = m - 1
    #not found
    return -1

#Test
string = "Makan ikan bakar itu enak sekali gaes mantap pisan"
pattern = "ikan"
result = stringMatchingBM(string,pattern)
if (result != -1):
    print("String ditemukan pada posisi indeks teks ke", result)
    print("String yang ditemukan adalah",string[result:result+len(pattern)])
