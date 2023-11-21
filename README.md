# **_TB-DROP_** 
## Introduction
- Aims the goal to end the global TB epidemic by 2030, which has been adopted by all Member States of the United Nations (UN) and the World Health Organization (WHO).
- Is an end-to-end, user-friendly, deep learning-based drug resistance prediction platform of *Mycobacterium tuberculosis* utilizing whole genome mutations.
## Installation
TB-DROP integrates with numbers of softwares commonly used in bioinformatics research, which needs to be run on linux. To simplify the installation of TB-DROP and its dependencies, we packaged TB-DROP into a Docker image, so that users needn't resolve the complex configuration of various softwares and TB-DROP could be used on any operating system that Docker supports.
### Docker Installation
Therefore, users must install Docker first. The installation of Docker could refer to the guideline in the official website of Docker (https://docs.docker.com/engine/install/). 
Some key points are listed below:
- Make sure that your computer's CPU supports virtualisation and WSL2 is installed. In regard to install WSL2, please refer to the following tutorial (https://aka.ms/wsl2kernel):  
- You can install your preferred linux system on WSL2 in the Microsoft Store after completing the installation of WSL2, and Ubuntu 20.04 is highly recommonded, because TB-DROP is developed based on Ubuntu 20.04.  
### Download  
Please create a folder `Docker` and downlocad all files required for TB-DROP ( `Dockerfile`, `pipeline.tar.gz` and `prepare_env.sh` ) to this directory from our latest release.
### Create Image
Launch command line mode and go into the folder `Docker`, then run: 
   
`docker build -t name_of_image .`    

Run `docker images`, find and remember the image ID of the image created before.  
- No capital letters in the name.
### Create Container & Run TB-DROP
To store the container, please create a folder other than the directory where the image is stored, and then move 
`pipeline.tar.gz` and `prepare_env.sh` to this folder. Then run:   
  
`docker run -p host_port:8080 -v path_to_store_container:/root/pipeline -itd image_ID /bin/bash -c "cd /root/pipeline;bash prepare_env.sh;touch finish;/bin/bash"`    

Creating a container for the first time takes a relatively long time because you need to decompress the compressed file 'pipeline.tar.gz' and prepare the environment.
- Parameters 'host_port' after `-p` can be freely specified. However, please remember the ports you specified, it's required when accessing the TB-DROP through localhost:host_port.   
- The `path_to_store_container` after `-v` must be absolute path.   
- When `finish` appears, installation has been completed, and then Docker will return the ID of the container, which is used to perform a series of operations, such as starting and deleting containers.
### Start TB-DROP
Visit `localhost:host port` in the browser, then you will see TB-DROP.
## Restart 
All data was saved in the container, so that you must restart the container created before rather than create a new container when you want to use TB-DROP again. The steps of restarting TB-DROP were listed below:  
1. Start Docker and launch the container created before in the container tab.  
2. Click the CLI botton to open a terminal.  
3. Run the following commands:  
  
&emsp; &emsp;`service mysql start`  
  
&emsp; &emsp;`nohup python3 /root/pipeline/tb-visualization/03.server/flask/run.py &> /dev/null &`  
  
4. Close the terminal and visit `localhost:host port` in the browser.
## Manual of TB-DROP  
##### Uploading:  
Fill in the sample ID and select the corresponding fastq files of the sample.Click `Submit`.  
##### Analyzing:  
Select the samples you want to analyze and Click `Start Analysis`.The status of sample will turn to `finished` when analysis is done. Click the sample ID then you will be redirected to the report page.
