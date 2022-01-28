import pickle
with open('questiondict_new.pickle','rb') as file:
    quer_resp = pickle.load(file)

# print(quer_resp)

for i,j in quer_resp.items():
    if i.find("\\n") != -1:
        v = i.replace("\\n","")
        quer_resp[v] = j
        quer_resp.pop(i)

    if j[1].find("\\n") != -1:
        v = j[1].replace("\\n","")
        quer_resp[i] = (j[0],v,j[2])

    if j[2].find("\\n") != -1:
        v = j[2].replace("\\n","")
        quer_resp[i] = (j[0],j[1],v)
        
for i,j in quer_resp.items():
    if i.find("\\n") != -1:
        print(i)

    if j[1].find("\\n") != -1:
        print(j[1])

    if j[2].find("\\n") != -1:
        print(j[2])

with open('questiondict_newcopy.pickle','wb') as file:
    pickle.dump(quer_resp,file)