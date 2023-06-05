import os
import json
                                #from os.path import isfile, join

                                # Laptop       root = "/Users/Honey/Documents/Github/zbmed-semtec.github.io/.github/workflows/"
                                #Laptop        rootMetadata = "/Users/Honey/Documents/Github/zbmed-semtec.github.io/.github/workflows/metadata/"
                                #testJsonErkennung = "/Users/Honey/Documents/Github/zbmed-semtec.github.io/.github/workflows/metadata/datasets/"

root = "C:/Users/Arbeit/Documents/GitHub/zbmed-semtec.github.io/"
rootMetadata = "C:/Users/Arbeit/Documents/GitHub\zbmed-semtec.github.io/metadata/"
rootDocs = "C:/Users/Arbeit/Documents/GitHub\zbmed-semtec.github.io/docs/"

listMetadata = os.listdir(rootMetadata)
print(listMetadata)
# Hier werden alle Subfolder von Metadata angegeben

                                #subfolderMetadata = [j for searchFolder in os.listdir(listMetadata)]
                                #test = any(isfile(join(os.path, i)) for i in rootMetadata)
                                #print(os.listdir(test))

                                #for i in listMetadata:
                                #    test = open(listMetadata)
                                #print(test)

listeTest = []
for i in listMetadata:
    subfolder = (rootMetadata + i + "/")
    listeTest.append(subfolder)
    print(subfolder)
    print(listeTest)
    # Hier wird die ganze Liste der Der Subfolder von Metadata an den Pfad angehängt



                                #for i in listMetadata:
                                #    print(rootMetadata +' test')

                                #searchJson = [posJsons for posJsons in os.listdir(testJsonErkennung) if posJsons.endswith('.json')]
                                #print(searchJson)


for i in listeTest:
    searchJson = [posJsons for posJsons in os.listdir(subfolder) if posJsons.endswith('.json')]
    print(searchJson)
                                #str(searchJson)
                                #print(type(searchJson))
                                #namensVergleich = str(searchJson)

    #Bis hierhin werden alle Files mit einem .json am Ende gesucht
   
    jsonString = json.dumps(searchJson)
                                #speicherJson = jsonString
    speicherJson = json.loads(jsonString)
    print(speicherJson)
    # abspeichern der json werte durch dumps in eine jsonString und dieser wird durch json.loads in variable abgespeichert um später auslesen zu können
                                #print(type(namensVergleich))

    namensVergleich = ' '.join(searchJson)

    print(namensVergleich)
    punktPosition = namensVergleich.index('.')
    geschnittenesWort = namensVergleich[:punktPosition]
    print(geschnittenesWort)

    #Die .json werden durch den join befehl wieder als String abgespeichert der befehl diesmal so um  den reinen Namen ohne Zeichen will 
    # ohne Sonderzeichen zu bekommen und diesem wird dann die .json endung abgeschnitten um gleich zu suchen

    os.chdir(rootDocs)
    #wechsel in den docs ordner 
                                 #print(os.getcwd())

    listDocs = os.listdir(rootDocs)
    for datei in listDocs:
        print(geschnittenesWort)
        if geschnittenesWort in datei:
            print("Test")
                                #subfolderDocs = (rootDocs + datei + "/")
                                #os.chdir(subfolderDocs)
                                #neueNamenMD = geschnittenesWort + ".md"
                                #with open(neueNamenMD, "w") as neueDateiMD:
                                #    neueDateiMD.write(speicherJson)    
    

        else:
            os.listdir(rootDocs)
            print("Test2")
            print(os.listdir(rootDocs))
            os.makedirs(os.path.join(rootDocs,geschnittenesWort))
            break

    # if bedingung bei der alle Inhalte des Ordners docs ausgegeben wird dieser wird durch überpruefung ob der klarname teil des Dateinamen ist
    # falls dies nicht der Fall ist so wird ein neuer Ordner im Verzeichnis rootDocs mit dem Namen geschnittenesWort kombiniert, der dann mit os.makedir kombiniert das Verzeichnis erstellt
    # falls der klarname teil eines Namen 