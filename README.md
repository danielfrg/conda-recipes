# conda recipes and tools

```
conda build <pkg>
```

## Linux

To get linux packages use the docker container. 

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

This image is based on [condaforge/linux-anvil](https://github.com/conda-forge/docker-images)
so packages that build here will probably build on conda-forge.

The subdirectories inside `cache` will be shared with the container to cache some things and make (re)builds faster:

- `conda-bld` so output packages are easy to access, it also helps a lot with debugging failed builds
- `conda-pkgs`: `/opt/conda/pkgs`   - This fails with a lot of files so currently disabled
- `maven`: `~/.m2`
