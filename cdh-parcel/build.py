import os
import re
import sys
import json
import shutil
from optparse import OptionParser
from subprocess import check_call


TMP_DIR = os.environ.get("PARCEL_TMP_DIR", "./tmp")
OUTPUT_DIR = os.environ.get("PARCEL_OUTPUT_DIR", "./output")
SUFFIX = os.environ.get("PARCEL_SUFFIX", "el6")

CONDA_ENV_SH = """#!/bin/bash
if [ -z "${CDH_PYTHON}" ]; then
export CDH_PYTHON=${PARCELS_ROOT}/${PARCEL_DIRNAME}/bin/python
fi
"""


def create(path):
    name, version = parse_path(path)

    # Clean tmp dir
    if os.path.exists(TMP_DIR):
        shutil.rmtree(TMP_DIR)
    assert not os.path.isdir(TMP_DIR)

    # Extract installer
    prefix = os.path.join(TMP_DIR, "%s-%s" % (name, version))
    check_call(["bash", path, "-b", "-p", prefix])

    # Fix shebang on `$PREFIX/bin` scripts
    fix_bin_dir(prefix)

    # Write extra parcel files
    meta_dir = os.path.join(prefix, "meta")
    if not os.path.exists(meta_dir):
        os.mkdir(meta_dir)
    packages = get_package_list(prefix)
    data = get_parcel_json(name, version, packages, SUFFIX)
    with open(os.path.join(meta_dir, "parcel.json"), "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)

    # Write parcel env scripts
    with open(os.path.join(meta_dir, "conda_env.sh"), "w") as f:
        f.write(CONDA_ENV_SH)

    # Tar directory into
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    outfile = "%s-%s-%s.parcel" % (name, version, SUFFIX)
    outfile = os.path.join(OUTPUT_DIR, outfile)
    check_call(["tar", "czf", os.path.abspath(outfile), os.path.basename(prefix)], cwd=TMP_DIR)
    print("Created:", outfile)


def parse_path(path):
    """
    Get name and version of the installer
    """
    pat = re.compile(r"([\w.]+)-([\w.]+)-Linux-x86_64\.sh$")
    fname = os.path.basename(path)
    match = pat.match(fname)
    name = match.group(1)
    version = match.group(2)
    return name, version


def get_package_list(prefix):
    """Get packages from an anaconda installation
    """
    packages = []

    # Get the (set of canonical names) of linked packages in prefix
    meta_dir = os.path.join(prefix, "conda-meta")
    pkg_list = set(fn[:-5] for fn in os.listdir(meta_dir) if fn.endswith(".json"))
    # print(pkgs)
    for dist in sorted(pkg_list):
        name, version, build = dist.rsplit("-", 2)
        packages.append({
            "name": name,
            "version": "%s-%s" % (version, build),
        })
    return packages


def fix_bin_dir(prefix):
    bin_dir = os.path.join(prefix, "bin")
    for fname in os.listdir(bin_dir):
        filepath = os.path.join(bin_dir, fname)
        if is_elf(filepath):
            continue
        fix_shebang(filepath)


def is_elf(filepath):
    if not os.path.isfile(filepath):
        return False
    with open(filepath, "rb") as file:
        head = file.read(4)
    return head == b"\x7fELF"


def fix_shebang(filepath):
    """
    Change the shebang to #!/usr/bin/env python
    """
    with open(filepath, "r") as f:
        script = f.read()

    shebang_pat = re.compile(r"^#!.+$", re.M)
    match = shebang_pat.match(script)
    if match and "python" in match.group():
        # If `python` its on the shebang, change it it the generic one
        new_script = shebang_pat.sub("#!/usr/bin/env python", script, count=1)
        if new_script == script:
            return
        print("Updating shebang on:", filepath)
        with open(filepath, "w") as file:
            file.write(new_script)
        os.chmod(filepath, 0o0755)


def get_parcel_json(name, version, packages, suffix):
    _ = {
        "schema_version": 1,
        "name": name,
        "version": version,
        "provides": [
            "anaconda",
        ],
        "scripts": {
            "defines": "conda_env.sh",
        },
        "packages": packages,
        "setActiveSymlink": True,
        "extraVersionInfo": {
            "fullVersion":"%s-%s" % (version, suffix),
            "baseVersion": version,
            "patchCount": "p0",
        },
        "components": [{
            "name": name,
            "version": version,
            "pkg_version": version,
        }],
        "users": {},
        "groups": [],
    }
    return _


def duplicate(path, symlink=False):
    """
    copy/symlink the generated parcel to distros
    """
    os.chdir(OUTPUT_DIR)

    name, version = parse_path(path)
    suffixes = ('el6', 'el7', 'sles11', 'sles12', 'jessie', 'lucid', 'precise', 'trusty','squeeze', 'wheezy')
    out_parcel_file = "%s-%s-%s.parcel" % (name, version, SUFFIX)
    # out_parcel_file = os.path.join(OUTPUT_DIR, out_parcel_filename)

    for suffix in suffixes:
        if suffix != SUFFIX:
            dst = out_parcel_file.replace('-{}'.format(SUFFIX), '-' + suffix)
            # dst = os.path.join(OUTPUT_DIR, dst)
            if symlink:
                print("Symlink:", out_parcel_file, dst)
                os.symlink(out_parcel_file, dst)
            else:
                print("Copy:", out_parcel_file, dst)
                shutil.copyfile(out_parcel_file, dst)


if __name__ == "__main__":
    p = OptionParser(
        usage="usage: %prog [options] PATH",
        description="create a parcel from an Anaconda installer (located at "
                    "PATH).  The resulting will be placed in the current "
                    "working directory")

    opts, args = p.parse_args()
    if len(args) != 1:
        p.error("Exactly one argument expected")

    installer_path = args[0]
    create(installer_path)
    duplicate(installer_path)
