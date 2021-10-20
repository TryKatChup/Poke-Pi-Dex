FROM tensorflow/tensorflow:latest-gpu
RUN apt-get update -y && apt-get install -y unzip curl \ 
    && pip install --upgrade pip && pip install jupyter sklearn matplotlib \
    black jupyter_contrib_nbextensions tqdm h5py \
    && jupyter nbextension install https://github.com/drillan/jupyter-black/archive/master.zip --user \
    && jupyter nbextension enable jupyter-black-master/jupyter-black


# Copy data
COPY ./data /app/data

# Unzip dataset
WORKDIR /app/data
RUN curl https://drive.google.com/u/0/uc?id=1B1kzsppgreGzB3qGde5BnLgpMogJPyKI&export=download \
&& unzip /app/data/archive.zip -d /app/data/ \
&& rm /app/data/archive.zip

# During development, the src folder will be overriden by a volume
COPY ./src /app/src

WORKDIR /app/src
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", \
     "--ip=0.0.0.0", "--allow-root"]

