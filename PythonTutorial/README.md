# Hoffman2 Python Tutorial

For basic information on Hoffman2, including submitting jobs, check job status, resources available, transfering files, and other general information, refer to the general guide <https://github.com/chris-german/Hoffman2Tutorials>.

This instruction is run using [`h2jupynb`](https://raw.githubusercontent.com/rdauria/jupyter-notebook/main/h2jupynb) script. On your terminal, save the linked python script, and you can run `python h2jupynb`. After typing in your password a couple of times, you will be running a Jupyter Notebook on Hoffman2. This is on a computer node. Keep your eyes on command-line arguments for the script; you can request GPU, more memory, more cores, etc. 

## Available Python Versions

There are several versions of Python on the cluster, with more up-to-date ones being installed as they are released and requested. 

We have a number of python versions installed:


```python
!module avail python
```

    ------------------------- [1;94m/u/local/Modules/modulefiles[0m -------------------------[m
    [1mpython[22m/2.7.15  [1mpython[22m/2.7.18  [1mpython[22m/3.6.8  [1mpython[22m/3.7.3  [4;90;47;1mpython[0;4;90;47m/3.9.6[0m  [m
    [m
    Key:[m
    [90;47mloaded[0m  [1;94mmodulepath[0m  [4mdefault-version[0m  [m
    [K[?1l>

And anaconda distributions are available as well, where you will be able to build your own environment from.


```python
!module avail anaconda
```

    ------------------------- [1;94m/u/local/Modules/modulefiles[0m -------------------------[m
    [1manaconda[22m2/2019.10  [4m[1manaconda[22m3/2020.11[0m  [1manaconda[22m3/2022.05  [m
    [1manaconda[22m3/2020.07  [1manaconda[22m3/2021.11  [1manaconda[22m3/2023.03  [m
    [m
    Key:[m
    [1;94mmodulepath[0m  [4mdefault-version[0m  [m
    [K[?1l>

## Loading Software

To load a module, say anaconda3 2023.03:


```python
!module load anaconda3/2023.03
```

If you are going to need packages installed for your use on Hoffman2, load anaconda module, activate your environment, and then install the packges. 

Note: If you ssh to `hoffman2.idre.ucla.edu`, this will be on the login node, where computing power is limited so you should not run any analyses on this node. Instead, you run analyses on a compute node. 

## Accessing a compute node

### qsub

For most analyses/jobs you'd like to run on Hoffman2, you should use the `qsub` command. This submits a batch job to the queue (scheduler). The type of file you `qsub` has to have a specific format (batch script).


Then we might want to use this bash script, with configurations on the top of the file.


```python
!cat submit.sh
```

    #!/bin/bash
    #$ -cwd #uses current working directory
    # error = Merged with joblog
    #$ -o joblog.$JOB_ID #creates a file called joblog.jobidnumber to write to. 
    #$ -j y 
    #$ -l h_rt=0:30:00,h_data=2G #requests 30 minutes, 2GB of data (per core)
    #$ -pe shared 2 #requests 2 cores
    # Email address to notify
    #$ -M $USER@mail #don't change this line, finds your email in the system 
    # Notify when
    #$ -m bea #sends you an email (b) when the job begins (e) when job ends (a) when job is aborted (error)
    
    # load the job environment:
    . /u/local/Modules/default/init/modules.sh
    module load anaconda #loads anaconda for use 
    
    # run Python code
    echo 'Running runSim.py' #prints this quote to joblog.jobidnumber
    python runSim.py 100 100 123 > output.$JOB_ID 2>&1
    # command-line arguments: number of samples, number of repetitions, seed
    # outputs any text (stdout and stderr) to output.$JOB_ID


To send this script to the scheduler to run on a compute node, you would simply type:


```python
!qsub submit.sh
```

    Your job 3422570 ("submit.sh") has been submitted


### qrsh

For some analyses, you may want to do things interactively instead of just submitting jobs. The `qrsh` command is for loading you onto an interactive compute node. 

Typing `qrsh` on the Hoffman2 login node will submit a request for an interactive session. By default, the session will run for two hours and the physical memory alotted will be 1GB.

To request more, you can use the commmand
```{bash}
qrsh -l h_rt=4:00:00,h_data=4G
```

This will request a four hour session where the maximum physical memory is 4GB. 
If you'd like to use more than one CPU core for your job, add `-pe shared #` to the end. Note, the amount of memory requested will be for each core. For example, if you'd like to request 4 CPU cores, each with 2GB of memory for a total of 8GB for 5 hours, run:
```{bash}
qrsh -l h_rt=5:00:00,h_data=2G -pe shared 4
```
The more time and memory you request, the longer you will have to wait for an interactive compute node to become available to you. It's normal to wait a few minutes to get an interactive session. 

__Note__: If you run the `h2jupynb` script, your request is going through the `qrsh` command. 

## Resource limitations

The maximum time for a session is 24 hours unless you're working in a group that owns their compute nodes. So do not have an `h_rt` value greated than `h_rt=24:00:00`.

Different compute nodes have different amounts of memory. There are fewer nodes with lots of memory, so the larger the amount of memory you're requesting the longer you will have to wait for the job to start running. If you request too much, the job may never run. 

Requesting more than 4 cores for an interactive session can possibly take a long time for the interactive session to start. 

## A single simulation run

The sample Python script [`runSim.py`](./runSim.py) runs a simulation study to estimate mean and standard deviation of a standard normal distribution. In each replicate, it generates a random vector of sample size `n`, a normal distribution, and using seed `s`. There are `reps` replicates. Values of `n`, `s`, and `reps` are defined by command-line arguments.



```python
!cat runSim.py
```

    import sys
    import os
    import numpy as np
    
    # number of samples per repeat
    n = int(sys.argv[1])
    # number of repetition
    reps = int(sys.argv[2])
    
    # seed
    seed = int(sys.argv[3])
    
    # create folder if it does not exist
    path = "simresults/"
    if not os.path.exists(path):
        os.makedirs(path)
    
    oFile = f"simresults/n_{n}_reps_{reps}_seed_{seed}.txt"
    
    # Simulate `reps` replicates of sample size `n` from distribution `d` using seed `seed`
    
    np.random.seed(seed)
    simres = np.zeros((reps, 2))
    for r in range(reps):
        x = np.random.randn(n)
        simres[r, 0] = np.mean(x)
        simres[r, 1] = np.std(x)
    
    np.savetxt(oFile, simres, delimiter=",")


To run this simulation from command line, user needs pass value for `n`, `reps`, and `s` via command-line argument. For example,
```{bash, eval=FALSE}
module load anaconda
python runSim.py 100 100 123
# command-line arguments: number of samples, number of repetitions, seed, command to create n samples
```
We can submit it to a compute node using the script [`submit.sh`](./submit.sh)
```{bash, eval=F}
qsub submit.sh
```

After the job is done, we can examine that the results have been written to the txt file.



```python
!head simresults/n_10_reps_10_seed_10.txt
```

    5.980830814078975932e-02,7.519756036909285291e-01
    1.776306496855655781e-01,9.076540062468508863e-01
    3.565352174694761400e-01,1.338380042592697938e+00
    9.305068510709016416e-02,6.833545782462973062e-01
    -1.745937595661832265e-01,5.120914533249217859e-01
    4.314985035350349385e-01,8.053695403228237071e-01
    -1.770132344449889539e-01,7.275438117945736138e-01
    1.605084543836911848e-01,1.079781951887012648e+00
    -1.979238315021951411e-01,1.371812535024111046e+00
    6.466563656045878905e-02,8.894817873225754346e-01


If you experience an error, you can take a look at the `output.####` file that was generated. This files indicates any output generated in Python. 

## Multiple simulation runs

In a typical simulation study, we vary the values of different simulation factors such as sample size, generative model, effect size, and so on. We can write a job script with jobarray setup to manage multiple simulations. It's easy to set up and perform embarrasingly parallel simulation tasks.

The syntax depends on the scheduling system. On UCLA's Hoffman2 cluster, `qsub` is used. In [`submit_array.sh`](./submit_array.sh), we loop over sample sizes `n` (100, 200, ..., 500). [`run_arrays.sh`](./run_arrays.sh) contains commands to submit multiple arrays with different seeds.



```python
!cat submitarray.sh
```

    #!/bin/bash
    #$ -cwd #uses current working directory
    # error = Merged with joblog
    #$ -o joblog.$JOB_ID.$TASK_ID #creates a file called joblog.jobidnumber.taskidnumber to write to. 
    #$ -j y 
    #$ -l h_rt=0:30:00,h_data=2G #requests 30 minutes, 2GB of data (per core)
    #$ -pe shared 2 #requests 2 cores
    # Email address to notify
    #$ -M $USER@mail #don't change this line, finds your email in the system 
    # Notify when
    #$ -m bea #sends you an email (b) when the job begins (e) when job ends (a) when job is aborted (error)
    #$ -t 100-500:100 # 100 to 500, with step size of 100
    
    # load the job environment:
    . /u/local/Modules/default/init/modules.sh
    module load anaconda
    
    echo ${SGE_TASK_ID}
    # run python code
    echo Running runSim.py for n = ${SGE_TASK_ID} #prints this quote to joblog.jobidnumber
    python runSim.py ${SGE_TASK_ID} 100 $1 > output.$JOB_ID.${SGE_TASK_ID} 2>&1



```python
!cat runarrays.sh
```

    qsub submit_array.sh 123
    qsub submit_array.sh 456
    qsub submit_array.sh 789
    qsub submit_array.sh 987


So on the cluster we just need to run



```python
!bash runarrays.sh
```

    Your job-array 3422834.100-500:100 ("submitarray.sh") has been submitted
    Your job-array 3422835.100-500:100 ("submitarray.sh") has been submitted
    Your job-array 3422839.100-500:100 ("submitarray.sh") has been submitted
    Your job-array 3422842.100-500:100 ("submitarray.sh") has been submitted


You can check on the state of your current jobs by running:



```python
!myjob
```

    job-ID     prior   name       user         state submit/start at     queue                          jclass                         slots ja-task-ID 
    ------------------------------------------------------------------------------------------------------------------------------------------------
       3422421 0.50001 JUPYNB     kose         r     06/04/2024 12:16:05 msa_smp.q@n7070                                                   1        



```python
!ls simresults/*.txt
```

    simresults/n_100_reps_10.txt  simresults/n_10_reps_10_seed_10.txt

