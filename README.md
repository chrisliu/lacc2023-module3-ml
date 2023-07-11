# LACC Module 3: AI & ML

## Contribute

### Environment Setup

For development, more packages, formatters, and Jupyter notebook support needs
to be installed. We'd recommend
[setting up a virtual environment](https://docs.python.org/3/library/venv.html)
first.

```bash
chmod u+x install-dev.sh && ./install-dev.sh
```

### Presenting from Jupyter Notebook

Once the environmennt is set up, you can launch Jupyter notebook

```bash
jupyter notebook
```

In Jupyter notebook, go to `View`>`Cell Toolbar` and select `Slideshow`. This
allows you to set the type of the slide.

`Option`/`Alt`+`R` enters presentation mode. Alternatively, you can click the
graph icon on the rightmost of the toolbar containing `Run`.

The basics of RISE is described in
[their documentation](https://rise.readthedocs.io/en/stable/usage.html).

### Git Basics

1. Add all changes that have been made.

```bash
git add -A
```

For finer control, you can directly specify the file or the directory (e.g.,
`git add .` for the current directory).

2. Write a commit message. It should be succint and informative.

```bash
git commit -m "your message"
```

Since we're using hooks, you may have to repeat the first two steps.

3. Push your commit to the remote repository (i.e., GitHub).

```bash
git push
```

If you run into any issues, try updating your local repository to the latest
copy.

```bash
git pull
```
