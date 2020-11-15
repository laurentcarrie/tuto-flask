from app import app
import subprocess
import click


@app.cli.group()
def translate():
    """ translation and localization commands """
    pass


@translate.command()
def update():
    """ update all languages """
    command = "pybabel extract -F babel.cfg -k _l -o messages.pot .".split()
    ret = subprocess.run(command)
    ret.check_returncode()

    command = "pybabel update -i messages.pot -d app/translations".split()
    ret = subprocess.run(command)
    ret.check_returncode()


@translate.command()
def compile():
    """ compile all languages """
    command = "pybabel compile -d app/translations".split()
    ret = subprocess.run(command)
    ret.check_returncode()


@translate.command()
@click.argument("lang")
def init(lang):
    """ initialize new language """
    command = "pybabel extract -F babel.cfg -k _l -o messages.pot .".split()
    ret = subprocess.run(command)
    ret.check_returncode()

    command = f"pybabel init -i messages.pot -d app/translations -l {lang}".split()
    ret = subprocess.run(command)
    ret.check_returncode()
