FROM condaforge/miniforge3:latest
LABEL maintainer "Asher Pembroke <apembroke@gmail.com>"

RUN pip install mkdocs python-markdown-math markdown-include pygments
RUN pip install mkdocs-material

WORKDIR /code

CMD mkdocs serve -a 0.0.0.0:8000

