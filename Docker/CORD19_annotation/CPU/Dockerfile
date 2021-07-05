FROM huggingface/transformers-pytorch-cpu
LABEL maintainer1="cbadenes@fi.upm.es"
LABEL maintainer2="alvaro.alonsoc@alumnos.upm.es"
LABEL version="0.1"
LABEL description="Bio-NLP CORD-19 Annotator"

COPY CORD-19_annotation/requirements.txt .
RUN pip install -r requirements.txt

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN python3 -m spacy download en_core_web_sm

ENV NUM_CORES='32'
ENV MKL_NUM_THREADS='32'
ENV OMP_NUM_THREADS='32'

COPY CORD-19_annotation/annotate_cord_19.py /app/CORD-19_annotation/annotate_cord_19.py
COPY CORD-19_annotation/utils.py /app/CORD-19_annotation/utils.py
COPY models/ /app/models/
COPY bionlp/ /app/bionlp/

WORKDIR /app/CORD-19_annotation

ENTRYPOINT ["python3"]
CMD ["annotate_cord_19.py", "normalize"]
