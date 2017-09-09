import os
import yaml
import glob
import shutil
import subprocess
from jinja2 import Environment, FileSystemLoader

args = {
    "version": "1.0.0.0",
    "constructor_version": "4.0.0",
    "anaconda_service_version": "1.0.0",
    "min_ambari_version": "2.4.0.0",
    "hdp_min_version": "2.0.*",
    "anaconda_dist_ext_version": "4.0.0",
    "min_stack_name": "HDP",
    "min_stack_version": "2.5.*",
}


def render_templates(output_dir="./output"):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    templates_dir = os.path.join(this_dir, "templates")

    # Cleanup: Remove output dir and create empty one
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.mkdir(output_dir)

    files = glob.iglob(os.path.join(templates_dir, "**/*"), recursive=True)
    jinja2_env = Environment(loader=FileSystemLoader(templates_dir))

    for fname in list(files):
        template_path = fname[len(templates_dir) + 1:]  # remove `./templates/` prefix
        print(template_path)
        output_path = os.path.join(output_dir, template_path)

        if os.path.isdir(fname):
            # Create dir in output
            output_path = Environment().from_string(output_path).render(**args)
            os.mkdir(output_path)
        else:
            # Render jinja template and save
            template = jinja2_env.get_template(template_path)
            output_from_parsed_template = template.render(**args)
            # Save file
            output_path = Environment().from_string(output_path).render(**args)
            with open(output_path, "w") as fh:
                fh.write(output_from_parsed_template)


def create_constructor(pkgs, output_dir="./output"):
    constructor_path = Environment().from_string("anaconda-mpack-{{ version }}/common-services/ANACONDA/{{ anaconda_service_version }}/package/files").render(**args)
    constructor_path = os.path.join(output_dir, constructor_path)

    spec = {
        "name": "Anaconda",
        "version": args["constructor_version"],
        "channels": ["http://repo.continuum.io/pkgs/free/"],
        "specs": pkgs
    }

    constructor_yml_file = os.path.join(constructor_path, "construct.yaml")
    with open(constructor_yml_file, "w") as fh:
        yaml.safe_dump(spec, fh, default_flow_style=False)
    process = subprocess.Popen(["constructor", "."], cwd=constructor_path)
    process.wait()


def pkg_extension(output_dir="./output"):
    tar_file = Environment().from_string("anaconda-mpack-{{ version }}.tar.gz").render(**args)
    target_dir = Environment().from_string("anaconda-mpack-{{ version }}").render(**args)
    process = subprocess.Popen(["tar", "-zcvf", tar_file, target_dir], cwd=output_dir)
    process.wait()


if __name__ == "__main__":
    output_dir = "./output"
    render_templates(output_dir=output_dir)
    pkgs = ["python 3.5*", "conda", "numpy", "pandas"]
    create_constructor(pkgs, output_dir=output_dir)
    pkg_extension(output_dir=output_dir)
