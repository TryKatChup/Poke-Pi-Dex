FROM tensorflow/tensorflow:latest-gpu
RUN apt-get update -y && apt-get install -y unzip curl graphviz \
    && pip install --upgrade pip && pip install jupyter sklearn pydot matplotlib \
    black jupyter_contrib_nbextensions tqdm h5py \
    && jupyter nbextension install https://github.com/drillan/jupyter-black/archive/master.zip --user \
    && jupyter nbextension enable jupyter-black-master/jupyter-black


# Copy data
COPY ./data /app/data

# Download dataset
RUN curl https://cloud.fuo.ninja/index.php/s/9mfWtjnEB77qsyj

# Unzip dataset
WORKDIR /app/data
RUN unzip /app/data/archive.zip -d /app/data/ && \
    rm /app/data/archive.zip

# During development, the src folder will be overriden by a volume
COPY ./src /app/src

WORKDIR /app/src
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", \
     "--ip=0.0.0.0", "--allow-root"]

