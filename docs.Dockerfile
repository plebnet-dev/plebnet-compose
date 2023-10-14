FROM condaforge/miniforge3:latest
LABEL maintainer "Asher Pembroke <apembroke@gmail.com>"

# use pip's --no-cache-dir option to avoid caching, which can reduce the image size
RUN pip install --no-cache-dir mkdocs python-markdown-math markdown-include pygments mkdocs-material

WORKDIR /code

CMD mkdocs serve -a 0.0.0.0:8000

