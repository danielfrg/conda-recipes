# Weird conda-recipes

```
conda-build <pkg>
```

## Linux

To get linux packages use the docker container:

Prepare:

```
make docker-image
```

Build:

```
make docker-run
```

Once in the container you can just do:

```
conda build <pkg>
```

The `conda-bld` directory is shared with the container so output packages are easy to access.

### Notes

The `cache` subdirectories will be shared with the container to cache some things and make some (re)builds faster:

- maven: `~/.m2`
