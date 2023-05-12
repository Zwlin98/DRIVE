import json

with open("criterion.json") as f:
    criterion = json.loads(f.read())

with open("drive.json") as f:
    drive = json.loads(f.read())

with open("hadolint.json") as f:
    hadolint = json.loads(f.read())

def check_equal(l1,l2):
    if set(l1) == set(l2):
        return True
    return False

D_TP,D_FP,H_TP,H_FP = 0,0,0,0
D_TN,D_FN,H_TN,H_FN = 0,0,0,0



for k,v in criterion.items():
    if len(v)>0:
        if check_equal(v,drive[k]):
            D_TP+=1
        else:
            D_FN+=1
        if check_equal(v,hadolint[k]):
            H_TP+=1
        else:
            H_FN+=1
    else:
        if len(drive[k]) == 0:
            D_TN+=1
        else:
            D_FP+=1
        if len(hadolint[k]) == 0:
            H_TN+=1
        else:
            H_FP+=1
        
print(D_TP,D_FP,H_TP,H_FP)
print(D_TN,D_FN,H_TN,H_FN)
D_P,H_P = round(D_TP/(D_TP+D_FP),3),round(H_TP/(H_TP+H_FP),3)
D_R,H_R = round(D_TP/(D_TP+D_FN),3),round(H_TP/(H_TP+H_FN),3)
D_F,H_F = round(2*(D_P*D_R)/(D_P+D_R),3),round(2*(H_P*H_R)/(H_P+H_R),3)

print("\t","D","\t","H")
print("P:\t",D_P,"\t",H_P)
print("R:\t",D_R,"\t",H_R)
print("F:\t",D_F,"\t",H_F)

