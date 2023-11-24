#!/bin/bash

sample_all=$1
left_1=$2
right_2=$3

outdir="/root/pipeline/tb-visualization/04.variant_calling"
filedir="/root/pipeline/tb-visualization/02.data"
software="/root/pipeline/tb-visualization/01.software"

source $software/env

left_path=${left_1//,/ }
right_path=${right_2//,/ }
sample_list=${sample_all//,/ }

sample_number=${#left_path[@]}

for ((i=0;i<${sample_number};i=i+1))
do
	#sample_message=(${left_path[i]//_/ })
	sample_name=${sample_list[i]}

	cd ${outdir}/05.sample_proprocessing
	rm -rf ${sample_name}
	mkdir ${sample_name};mkdir ${sample_name}/tmp
	rm -f ${sample_name}/status

	fastp -i ${filedir}/${left_path[i]} -I ${filedir}/${right_path[i]} \
	 -o ${sample_name}/tmp/${sample_name}.clean.1.fq -O ${sample_name}/tmp/${sample_name}.clean.2.fq \
	 -h ${sample_name}/tmp/${sample_name}.html  -w 8
        
        ##echo "** The quality control of the raw sequence is completed **"	

	bwa-mem2  mem  -t 8 -R "@RG\tID:${sample_name}\tPL:Illumina\tSM:${sample_name}"  \
	${outdir}/00.index/bwa-mem2/H37Rv  \
	${sample_name}/tmp/${sample_name}.clean.1.fq   ${sample_name}/tmp/${sample_name}.clean.2.fq | samtools sort  \
	-O bam -o  ${sample_name}/tmp/${sample_name}.bam \
	&& sambamba  markdup -t 6 ${sample_name}/tmp/${sample_name}.bam  ${sample_name}/tmp/${sample_name}.markdup.bam
	
	##echo "** mapping done && BAM sort done && markdup done **"

	gatk HaplotypeCaller  \
	-R ${outdir}/00.index/gatk/H37Rv.fasta  \
	-I ${sample_name}/tmp/${sample_name}.markdup.bam  \
	-O ${sample_name}/tmp/${sample_name}.raw.vcf

	gatk SelectVariants \
	-select-type SNP \
	-V ${sample_name}/tmp/${sample_name}.raw.vcf \
	-O ${sample_name}/tmp/${sample_name}.snp.vcf

	gatk SelectVariants \
	-select-type INDEL \
	-V ${sample_name}/tmp/${sample_name}.raw.vcf \
	-O ${sample_name}/tmp/${sample_name}.indel.vcf

	gatk VariantFiltration \
	-V ${sample_name}/tmp/${sample_name}.snp.vcf \
	--filter-expression "QD < 2.0 || FS > 60.0 || MQ < 40.0 || SOR > 3.0 || MQRankSum < -12.5 || ReadPosRankSum < -8.0"  \
	--filter-name "Filter" \
	-O ${sample_name}/tmp/${sample_name}.snp.filter.vcf

        gatk VariantFiltration \
	-V ${sample_name}/tmp/${sample_name}.indel.vcf \
	--filter-expression "QD < 2.0 || FS > 200.0 || SOR > 3.0 || ReadPosRankSum < -20.0"  \
	--filter-name "Filter" \
	-O ${sample_name}/tmp/${sample_name}.indel.filter.vcf	
	
	gatk MergeVcfs \
	-I ${sample_name}/tmp/${sample_name}.snp.filter.vcf \
	-I ${sample_name}/tmp/${sample_name}.indel.filter.vcf \
	-O ${sample_name}/tmp/${sample_name}.filter.vcf

	vcftools  --vcf  ${sample_name}/tmp/${sample_name}.filter.vcf  --remove-filtered-all  \
	--recode  --stdout > ${sample_name}/${sample_name}.pass.vcf 

	perl ${software}/annovar/convert2annovar.pl  -format vcf4 ${sample_name}/${sample_name}.pass.vcf \
	-out ${sample_name}/${sample_name}.avinput

	perl ${software}/annovar/annotate_variation.pl  -geneanno -dbtype refGene -out ${sample_name}/${sample_name} \
	-build H37Rv ${sample_name}/${sample_name}.avinput   ${software}/annovar/mtbdb/

	#echo "** variant calling finished **"
	
	rm -r ${sample_name}/tmp

	rm -f ${outdir}/05.sample_proprocessing/fastp.json
	rm -f ${outdir}/05.sample_proprocessing/${sample_name}/{sample_name}.log
	rm -f ${outdir}/05.sample_proprocessing/out.log

	python3 ${outdir}/100bp.py  $sample_name

	python3 $software/dl_model/load_predict.py   $sample_name/data_format.csv    $sample_name

	#touch ${sample_name}/status
	report_file=/root/pipeline/tb-visualization/05.drug_resistance_prediction/$sample_name
	if [ ! -s "${report_file}" ];then
		echo "error"  > ${outdir}/05.sample_proprocessing/${sample_name}/status
	else
		echo "finished"  > ${outdir}/05.sample_proprocessing/${sample_name}/status
	fi


done

