FROM huggingface/transformers-pytorch-cpu
LABEL maintainer1="cbadenes@fi.upm.es"
LABEL maintainer2="alvaro.alonsoc@alumnos.upm.es"
LABEL version="0.1"
LABEL description="Bio-NLP Webapp"

COPY requirements.txt .
RUN pip install -r requirements.txt

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN python3 -m spacy download en_core_web_sm

COPY app.py /app/
COPY models/ /app/models/
COPY bionlp/ /app/bionlp/
COPY templates /app/templates/
COPY static /app/static/
WORKDIR /app
ENTRYPOINT ["python3"]
CMD ["app.py"]
