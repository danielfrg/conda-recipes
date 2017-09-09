# Anaconda mpack for Ambari

Ambari management pack builder for Anaconda

## Build the pack

The `build.py` script will create an `output` directory what contains the extension pack as a `.tar.gz` file in the
`output` directory.

```
$ python build.py

$ ls output
anaconda-mpack-1.0.0.0
anaconda-mpack-1.0.0.0.tar.gz
```

NOTE: The script works in all OS but since ambari is a Hadoop distribution that is installed on Linux this means
it usually requires a Linux version of the Anaconda distribution.

If not on Linux a helper Dockerfile is provided to generate a valid Linux Anaconda distribution and amabari mpack.

```
# Build the container
$ docker build -t ambari-extensions .

# Start it and share this directory as a volume
$ docker run -it -v $(pwd):/ambari-extensions ambari-extensions

# Build the pack
$ python build.py
```

## Options

The options can be found in the `build.py` this includes versions and list of packages in the distribution.

## Installation

Move the `.tar.gz` to the ambari server node, for example using scp:

```
$ scp -i ~/.ssh/keypair.pem anaconda-mpack-1.0.0.0.tar.gz centos@ambari-server:.
```

Install the extension pack

```
$ ambari-server install-mpack --mpack=anaconda-mpack-1.0.0.0.tar.gz

# Restart amabari-server
$ ambari-server restart
```

After all this the `Anaconda` service will show up on the services list at: http://ambari-server:8080/#/main/admin/stack/services
and it can be added to the cluster.

### Upgrade

Change the version of the mpack in the `build.py` script upload and then upgrade:

```
$ ambari-server upgrade-mpack --mpack=anaconda-mpack-1.1.0.0.tar.gz

# Restart amabari-server
$ ambari-server restart
```
