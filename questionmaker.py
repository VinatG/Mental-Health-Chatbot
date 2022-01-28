import pickle
def recr_ques(ques_dict,question=None):
    if question == '' or question in ques_dict:
        return
    if len(ques_dict) == 0:
        cur_question = input("Enter question: ")
    else:
        cur_question = question
    print("Enter response score for:",cur_question)
    res_score = input()
    print("Enter ques when >=",res_score)
    T_ques = input()
    print("Enter ques when <",res_score)
    F_ques = input()
    tup = (float(res_score) if res_score != '' else '',T_ques,F_ques)
    ques_dict[cur_question] = tup
    recr_ques(ques_dict,T_ques)
    recr_ques(ques_dict,F_ques)

def main():
    listofq={}
    recr_ques(listofq)

    with open('questiondict_new.pickle','wb') as file:
        pickle.dump(listofq,file)

if __name__ == "__main__":
    main()