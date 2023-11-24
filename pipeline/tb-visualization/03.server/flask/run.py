from website import app
import os
# 2021/8/24 ---1.1
if __name__ == '__main__':
    # app.run(debug=True, port=13347, host='0.0.0.0')
    os.environ['PATH'] = "/root/tb-visualization/01.software/gatk-4.2.0.0:/root/tb-visualization/01.software/sambamba-0.8.0:/root/tb-visualization/01.software/samtools-1.11:/root/tb-visualization/01.software/fastp-0.20.1:/root/tb-visualization/01.software/bwa-mem2-2.2.1_x64-linux:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/root/tb-visualization/01.software/jre1.8.0_281/bin"
    app.run(debug=True,port=8080,host='0.0.0.0')
