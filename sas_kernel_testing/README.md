Docker setup to test connection to a remote SAS installation via `saspy` and `sas_kernel`.

Build container:

```
$ docker build -t sas_kernel-test .
```

Start container

```
$ docker run -it -p 8888:8888 -v $(pwd):/work sas_kernel-test
```

In a console in Jupyter Lab:

```
$ eval `ssh-agent -s`
$ ssh-add adam.pem  # or whatever keypair to ssh to the node
```

Modify `sascfg_personal.py` if needed and move it to You need to move this file to either ot this:

- `/opt/conda/lib/python3.6/site-packages/sascfg_personal.py`  # saspy > 2.1.6
- `/opt/conda/lib/python3.6/site-packages/saspy/sascfg_personal.py`

The notebooks have examples on how to run it.
