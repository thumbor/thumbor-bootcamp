import os
import subprocess
from os.path import abspath, dirname, join
from pathlib import Path
from typing import Optional, Tuple

import click
import requests
from github import Github
from github.GithubException import UnknownObjectException
from github.Label import Label
from github.Repository import Repository
from jinja2 import Environment, FileSystemLoader, select_autoescape


@click.command()
@click.option("--count", default=1, help="Number of issues to create.")
@click.option(
    "--template",
    default="mypy-issue.md",
    help="The path to the template to create the issue with",
)
@click.option(
    "--thumbor-dir",
    default="../thumbor",
    help="The path to thumbor's repository",
)
def mypy_issues(
    count: int = 1, template: str = "mypy-issue.md", thumbor_dir: str = "../thumbor"
) -> None:
    """
    Program that creates new issues for every
    mypy violation in the repository
    """
    loader = FileSystemLoader(abspath(join(dirname(__file__), "./templates")))
    env = Environment(loader=loader, autoescape=select_autoescape())
    issue_template = env.get_template(template)

    all_files = []
    modules = ["thumbor", "tests"]

    for modules_prefix in modules:
        all_files += list(Path(f"{thumbor_dir}/{modules_prefix}").rglob("*[.]py"))

    processed_files = 0
    created_issues = 0

    while created_issues < count:
        if processed_files >= len(all_files):
            print("- ran out of files to submit...")

            return

        current_file = str(all_files[processed_files])
        print(f"- verifying {current_file}...")
        module_prefix = dirname(dirname(current_file))
        filepath = join(current_file.replace(module_prefix + "/", ""))

        if has_issue(filepath):
            print(
                f"- issue for mypy verification for file {filepath} already exists. Skipping..."
            )
            processed_files += 1

            continue

        exit_code, result = run_mypy(thumbor_dir, current_file)
        issue_body = issue_template.render(
            filepath=filepath,
            mypy_exit_code=exit_code,
            mypy_output=result.replace(f"./{module_prefix}/", ""),
        )

        if exit_code != 0:
            print(f"- mypy violations found in {current_file}. Creating issue...")
            url = create_issue(filepath, issue_body)
            print(f"- issue { url } created successfully.")
            created_issues += 1

        processed_files += 1


def run_mypy(thumbor_dir: str, filepath: str) -> Tuple[int, str]:
    mypy_sh = abspath(join(dirname(__file__), "mypy.sh"))
    with subprocess.Popen(
        ["/bin/bash", mypy_sh, f"-f {filepath}", f"-c {thumbor_dir}/mypy.ini"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ) as result:
        stdout, _ = result.communicate()
        return_code = result.returncode

        return return_code, stdout.decode("utf-8")


def has_issue(filepath: str) -> bool:
    client = Github(os.environ.get("THUMBOR_BOOTCAMP_ACCESS_TOKEN"))
    repo = client.get_repo("thumbor/thumbor-bootcamp")
    issues = repo.get_issues(state="open", labels=["mypy", filepath])

    return issues.totalCount != 0


def create_issue(filepath: str, contents: str) -> str:
    client = Github(os.environ.get("THUMBOR_BOOTCAMP_ACCESS_TOKEN"))
    repo = client.get_repo("thumbor/thumbor-bootcamp")
    labels = []

    for label_name in ["task", "L1", "mypy", filepath]:
        print(f"- looking for label {label_name}...")
        label = get_label(repo, label_name)

        if label is None:
            print(f"- label { label_name } was not found. Creating...")
            url = create_label(
                label_name, "CCCCCC", "label for fixing issues with the specified file"
            )
            print(f"- created new label { url }.")
        else:
            print(f"- label { label_name } found.")

        labels.append(label_name)

    print("- creating issue...")
    issue = repo.create_issue(
        title=f"[Bootcamp Task] Implement static typing for {filepath}",
        body=contents,
        labels=labels,
    )

    return issue.url


def get_label(repo: Repository, label_name: str) -> Optional[Label]:
    try:
        return repo.get_label(label_name)
    except UnknownObjectException:
        return None


def create_label(name: str, color: str, description: str) -> str:
    #  curl \
    #  -X POST \
    #  -H "Accept: application/vnd.github.v3+json" \
    #  https://api.github.com/repos/octocat/hello-world/labels \
    #  -d '{"name":"name"}'
    url = "https://api.github.com/repos/thumbor/thumbor-bootcamp/labels"
    session = requests.Session()
    session.auth = (
        str(os.environ.get("THUMBOR_BOOTCAMP_USER")),
        str(os.environ.get("THUMBOR_BOOTCAMP_ACCESS_TOKEN")),
    )

    response = session.post(
        url,
        json={"name": name, "color": color, "description": description},
        headers={
            "Content-Type": "application/json",
            "Accept": "application/vnd.github.v3+json",
        },
    )

    if response.status_code != 201:
        raise RuntimeError(
            f"Could not create label {name}. Error: {str(response.content)}"
        )

    return response.json()["url"]


if __name__ == "__main__":
    mypy_issues()
