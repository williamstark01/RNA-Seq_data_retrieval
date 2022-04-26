# RNA-Seq data retrieval

Download RNA-Seq samples and metadata from ENA.


## run script manually

```
python download_ena_samples.py --taxon_id <taxon_id>

# e.g.
# salmon taxon_id
python download_ena_samples.py --taxon_id 8030
```


## create Singularity image

build Docker image
```
docker image build --tag williamebi/rna_seq_data_retrieval --file Dockerfile .
```

upload Docker image to Docker Hub
```
docker push williamebi/rna_seq_data_retrieval
```

generate Singularity image from the Docker image
```
singularity pull docker://williamebi/rna_seq_data_retrieval
```


## download metadata with Singularity

```
SINGULARITY_IMAGE=<Singularity image path>; OUTPUT_DIRECTORY=<output directory>; TAXON_ID=<taxonomy ID>; singularity run --bind "$OUTPUT_DIRECTORY":/data "$SINGULARITY_IMAGE" --taxon_id "$TAXON_ID"
```
