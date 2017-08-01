Run only in Linux

Most likely you want to run this on the docker image from the root of this repo

## Before creating

Setup the validation tools:

```
make setup
```

## Building

Edit the `construct.yaml` file to include the packages you want in the parcel.

```
make

# its the same as
make installer
make parcel
```

## Serve the files
