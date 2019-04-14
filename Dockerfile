FROM pamamu/s2t_main-controller

ARG SHARED_FOLDER
ENV SHARED_FOLDER = $SHARED_FOLDER
ARG SRILM_NAME
ENV SRILM_NAME = $SRILM_NAME

WORKDIR /srv/S2T/S2T_SRILM

ADD . .

RUN pip install -r requirements.txt

CMD python src/app.py $SRILM_NAME $SHARED_FOLDER


