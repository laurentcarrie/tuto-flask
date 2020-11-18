import click
import subprocess
import re
from pprint import pp

ps_columns = {
    "CONTAINER ID": None,
    "IMAGE": None,
    "COMMAND": None,
    "CREATED": None,
    "STATUS": None,
    "PORTS": None,
    "NAMES": None,
}
re_ps_header = re.compile(
    "(CONTAINER ID)\s+(IMAGE)\s+(COMMAND)\s+(CREATED)\s+(STATUS)\s+(PORTS)\s+(NAMES)"  # noqa W605
)


def get_ps(image):
    """ see processes """
    command = "sudo docker ps --all"
    click.echo(command)
    output = subprocess.run(command.split(), capture_output=True)
    output.check_returncode()
    lines = output.stdout.decode().split("\n")
    header = lines[0]
    lines = lines[1: len(lines) - 1]
    if re_ps_header.match(header) is None:
        raise Exception("title line not matched")
    for key in ps_columns.keys():
        ps_columns[key] = {"start": header.find(key)}
    for key in ps_columns.keys():
        start = ps_columns[key]["start"]
        ends = [
            value["start"] for _, value in ps_columns.items() if value["start"] > start
        ]
        if ends == []:
            end = None
        else:
            end = min(ends)
        ps_columns[key].update({"end": end})

    all = []
    for line in lines:
        data = {}
        for key, pos in ps_columns.items():
            data[key] = line[pos["start"]: pos["end"]].strip()
        if image and image not in data["IMAGE"]:
            continue
        all.append(data)
    return all


@click.group()
def main():
    """ main """
    pass


@main.command()
@click.option("--image")
def ps(image):
    """ see processes """
    all = get_ps(image)
    for data in all:
        click.echo(data)


@main.command()
@click.option("--image")
def stop(image):
    """ stop processes """
    all = get_ps(image)
    for data in all:
        command = f"sudo docker stop {data['CONTAINER ID']}"
        click.echo(command)
        output = subprocess.run(command.split(), capture_output=True)
        output.check_returncode()


@main.command()
@click.option("--image")
def rm(image):
    """ rm processes """
    all = get_ps(image)
    for data in all:
        command = f"sudo docker rm {data['CONTAINER ID']}"
        click.echo(command)
        output = subprocess.run(command.split(), capture_output=True)
        output.check_returncode()


@main.command()
def current(location, api_key):
    """ current """
    pass


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        exit(1)
