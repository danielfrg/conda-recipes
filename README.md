# Weird conda-recipes

```
conda build <pkg>
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

### Notes

The `conda-bld` directory is shared with the container so output packages are easy to access.
This also helps a lot with debugging failed builds.

The `cache` subdirectories will be shared with the container to cache some things and make some (re)builds faster:

- `conda-pkgs`: `/opt/conda/pkgs`   - This fails with a lot of files so currently disabled
- `maven`: `~/.m2`
