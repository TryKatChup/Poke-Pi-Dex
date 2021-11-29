FROM tensorflow/tensorflow:2.6.0-gpu-jupyter
RUN apt-get update -y && apt-get install -y unzip wget graphviz \
    && pip install --upgrade pip && pip install sklearn pydot matplotlib \
    && pip install --pre torch torchvision torchaudio -f https://download.pytorch.org/whl/nightly/cu113/torch_nightly.html

# Copy data
COPY ./data /app/data

# Unzip dataset
WORKDIR /app/data
# https://cloud.fuo.ninja/index.php/s/qnzW7zrzeBf2s8J/download/archive.zip
# dataset brutto jGaqWaQSAk6zAo2
# dataset mezzo bello https://cloud.fuo.ninja/index.php/s/zjMiBt8R2a7ygpT/download/archive.zip
# Download dataset
RUN wget https://cloud.fuo.ninja/index.php/s/qnzW7zrzeBf2s8J/download/archive.zip -O /app/data/archive.zip \
&& unzip /app/data/archive.zip -d /app/data/ && \
rm /app/data/archive.zip

# During development, the src folder will be overriden by a volume
COPY ./src /app/src

WORKDIR /app/src
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", \
     "--ip=0.0.0.0", "--allow-root"]

