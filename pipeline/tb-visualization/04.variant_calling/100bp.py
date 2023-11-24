from itertools import groupby
import sys

peppe={}
with open('/root/pipeline/tb-visualization/04.variant_calling/00.index/peppe.txt', 'r') as peppe_file:
    for peppe_posi in peppe_file:
        peppe[peppe_posi.strip()] = ''

sample=sys.argv[1]
sample_allposi = {}
sample_sys = {}
smaple_all_path='/root/pipeline/tb-visualization/04.variant_calling/05.sample_proprocessing/' + sample.strip() +'/'+ sample.strip()+'.variant_function'
smaple_sys_path = '/root/pipeline/tb-visualization/04.variant_calling/05.sample_proprocessing/' + sample.strip() +'/'+ sample.strip()+ '.exonic_variant_function'
with open(smaple_all_path, 'r') as posi_infile:
    for line in posi_infile:
        sample_allposi[line.split('\t')[3]]=''
with open(smaple_sys_path, 'r') as ann_infile:
    for line2 in ann_infile:
        if 'synonymous SNV' in line2:
            pass
        else :
            sample_sys[line2.split('\t')[4]]=''
for sys_key in sample_sys.keys():
    if sys_key in sample_allposi:
        del sample_allposi[sys_key]
for peppe_key in peppe:
    if peppe_key in sample_allposi:
        del sample_allposi[peppe_key]

sample_posi = []
for n in sample_allposi.keys():
    sample_posi.append(eval(n))
final_dic={}
for n in range(0 ,44116):
    string=str(n*100)+'-'+str((n+1)*100+1)
    final_dic[string]=0

dic = {}
for k, g in groupby(sample_posi, key=lambda x: x  // 100):
     dic['{}-{}'.format(k * 100 , ((k + 1) * 100)+1)] = len(list(g))
final_dic.update(dic)

alldata = list(final_dic.values())
with open('/root/pipeline/tb-visualization/04.variant_calling/05.sample_proprocessing/' + sample.strip() +'/'+'data_format.csv', 'a+') as f:
    f.write(str(alldata).replace('[','').replace(']','\n'))
