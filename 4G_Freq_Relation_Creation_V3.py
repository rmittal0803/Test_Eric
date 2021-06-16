import datetime
import time
import os.path
import shutil
date=datetime.date.today()
pa=os.getcwd()
loc=raw_input('Enter file name/location/.txt: ')
cv_name=raw_input('Enter CV Name: ')
output=raw_input('Enter directory name: ')
s_time=time.time()
#save=os.getcwd()+"\"+raw_input('Enter directory name: ')
save=os.path.join(pa,output)
print(save)
if os.path.isdir(save):
    shutil.rmtree(save)
    os.mkdir(save)
else:
    os.mkdir(save)        
#path=os.path.join(pa,output)
#os.mkdir(path)
#open location & store lines in dictionary with nested list
f=open(loc,'r')
lines=f.read().splitlines()
d={}
for line in lines:
    if len(line)>0:
        temp=line.split('\t')
        c=list(filter(None,temp))
        if d.get(c[0]) is None:
            d[c[0]]=[]
        d[c[0]].append(c[1:])
#print(d)
sum=0
a=0
#read dictionary & create files
error={}
for i in d.keys():
    print(i,len(d[i]))
    sum+=len(d[i])
    new_file=os.path.join(save,str(i)+'.cmd')
    f=open(new_file,'wt')
    a+=1
    f.write("lt all\nrbs\nrbs\nalt\nst cell\ngsg+\nconfb+\ncvls\ncvms pre_"+cv_name+"_"+str(date)+"\n\n")
    #print (d[i])
    #f.write('\n'.join(d[i]))
    #print('list test')
    #create freq relation cell wise
    for freq in d[i]:
        if len(freq)<3:
            if error.get(i) is None:
                error[i]=[]
            error[i].append(freq)
            continue
        #print(freq)
        cell=freq[0]
        frequency=freq[1]
        resel=freq[2]
        f.write("cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency="+frequency+"\n"+frequency+"\n\ncr ENodeBFunction=1,"+cell+",EUtranFreqRelation="+frequency+"\nENodeBFunction=1,EUtraNetwork=1,EUtranFrequency="+frequency+"\n"+resel+"\n\n")
    f.write("\n\ncvms post_"+cv_name+"_"+str(date)+"\ncvls\nst cell\nq")
    f.close()
#print(error)
error_file=os.path.join(pa,'input_errors.txt')
error_node=open(error_file,'wt')
for er in error.keys():
    #for err in error[er]:
    for i in error[er]:
        a=', '.join(i[:])
        #error_node.write("{}:\t{}\n".format(er,a))
        error_node.write(er+"\t"+a)
error_node.close()
d_node=os.path.join(save,'allnode.txt')
f_node=open(d_node,'wt')
for j in d.keys():
    f_node.write("%s\n"%j)
f_node.close()
p=int(raw_input('Enter Required No of Parllel Process: '))
t=int(raw_input('Enter Timeout: '))
#command='amosbatch -p %d -t %d %s %s. %s'%(p,t,d_node,save,save)
command='amosbatch -p %d -t %d %s %s/. %s/%s_logs'%(p,t,d_node,save,pa,output)
print('Total nodes:',a,'Total rows:',sum)
print('Output Directory: ',save)
print('Mobatch Command: \n'+command)
print(time.time()-s_time)
