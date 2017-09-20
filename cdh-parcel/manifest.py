import os
import re
import time
import json
import tarfile
import hashlib
import posixpath
from optparse import OptionParser


OUTPUT_DIR = os.environ.get("PARCEL_OUTPUT_DIR", "./output")


def _get_parcel_dirname(parcel_name):
    """
    Extract the required parcel directory name for a given parcel.
    eg: CDH-5.0.0-el6.parcel -> CDH-5.0.0
    """
    parts = re.match(r"^(.*?)-(.*)-(.*?)$", parcel_name).groups()
    return parts[0] + '-' + parts[1]


def _safe_copy(key, src, dest):
    """
    Conditionally copy a key/value pair from one dictionary to another.
    Nothing is done if the key is not present in the source dictionary
    """
    if key in src:
        dest[key] = src[key]


def make_manifest(path, timestamp=time.time()):
    """
    Make a manifest.json document from the contents of a directory.
    This function will scan the specified directory, identify any parcel files
    in it, and then build a manifest from those files. Certain metadata will be
    extracted from the parcel and copied into the manifest.

    @param path: The path of the directory to scan for parcels
    @param timestamp: Unix timestamp to place in manifest.json
    @return: the manifest.json as a string
    """
    manifest = {}
    manifest['lastUpdated'] = int(timestamp * 1000)
    manifest['parcels'] = []

    files = os.listdir(path)
    for fname in files:
        if not fname.endswith('.parcel'):
            continue

        print('Found parcel %s' % (fname,))
        entry = {}
        entry['parcelName'] = fname

        fullpath = os.path.join(path, fname)

        with open(fullpath, 'rb') as fp:
            entry['hash'] = hashlib.sha1(fp.read()).hexdigest()

        with tarfile.open(fullpath, 'r') as tar:
            try:
                json_member = tar.getmember(posixpath.join(_get_parcel_dirname(fname), 'meta', 'parcel.json'))

            except KeyError:
                print("Parcel does not contain parcel.json")
                continue
            try:
                parcel = json.loads(tar.extractfile(json_member).read().decode(encoding='UTF-8'))
            except:
                print("Failed to parse parcel.json")
                continue
            _safe_copy('depends', parcel, entry)
            _safe_copy('replaces', parcel, entry)
            _safe_copy('conflicts', parcel, entry)
            _safe_copy('components', parcel, entry)
            _safe_copy('servicesRestartInfo', parcel, entry)

            try:
                notes_member = tar.getmember(posixpath.join(_get_parcel_dirname(fname),
                                                            'meta', 'release-notes.txt'))
                entry['releaseNotes'] = tar.extractfile(notes_member).read().decode(encoding='UTF-8')
            except KeyError:
                # No problem if there's no release notes
                pass

        manifest['parcels'].append(entry)

    return manifest


def write_parcel(data, path):
    content = json.dumps(data, indent=4, separators=(',', ': '), sort_keys=True)

    fpath = os.path.join(path, 'manifest.json')
    with open(fpath, 'w') as file:
        file.write(content)


if __name__ == "__main__":
    p = OptionParser(
        usage="usage: %prog [options]",
        description="Create the manifest.json from a directory of parcels")

    manifest = make_manifest(path=OUTPUT_DIR)
    write_parcel(manifest, path=OUTPUT_DIR)
