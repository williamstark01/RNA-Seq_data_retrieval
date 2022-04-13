# See the NOTICE file distributed with this work for additional information
# regarding copyright ownership.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Download RNA-Seq samples and metadata from ENA.
"""


# standard library imports
import argparse
import sys

# third party imports
import requests

# project imports


# fields currently used in the eHive module
original_fields = [
    "run_accession",
    "study_accession",
    "experiment_accession",
    "sample_accession",
    "secondary_sample_accession",
    "instrument_platform",
    "instrument_model",
    "library_layout",
    "library_strategy",
    "read_count",
    "base_count",
    "fastq_ftp",
    "fastq_aspera",
    "fastq_md5",
    "library_source",
    "library_selection",
    "center_name",
    "study_alias",
    "experiment_alias",
    "experiment_title",
    "study_title",
]

# additional fields that seem to be useful in identifying a proper sample source name
additional_fields = [
    "tissue_type",
]

# all_fields - (original_fields + additional_fields)
remaining_fields = [
    "secondary_study_accession",
    "submission_accession",
    "tax_id",
    "scientific_name",
    "library_name",
    "nominal_length",
    "first_public",
    "last_updated",
    "run_alias",
    "fastq_bytes",
    "fastq_galaxy",
    "submitted_bytes",
    "submitted_md5",
    "submitted_ftp",
    "submitted_aspera",
    "submitted_galaxy",
    "submitted_format",
    "sra_bytes",
    "sra_md5",
    "sra_ftp",
    "sra_aspera",
    "sra_galaxy",
    "cram_index_ftp",
    "cram_index_aspera",
    "cram_index_galaxy",
    "sample_alias",
    "broker_name",
    "nominal_sdev",
    "first_created",
    "sample_description",
    "parent_study",
    "library_construction_protocol",
    "accession",
    "bio_material",
    "cell_line",
    "cell_type",
    "collected_by",
    "collection_date",
    "country",
    "cultivar",
    "culture_collection",
    "description",
    "dev_stage",
    "ecotype",
    "environmental_sample",
    "germline",
    "identified_by",
    "isolate",
    "isolation_source",
    "location",
    "mating_type",
    "serotype",
    "serovar",
    "sex",
    "submitted_sex",
    "specimen_voucher",
    "strain",
    "sub_species",
    "sub_strain",
    "tissue_lib",
    "variety",
    "checklist",
    "depth",
    "elevation",
    "altitude",
    "environment_biome",
    "environment_feature",
    "environment_material",
    "temperature",
    "salinity",
    "sampling_campaign",
    "sampling_site",
    "sampling_platform",
    "protocol_label",
    "project_name",
    "host",
    "host_tax_id",
    "host_status",
    "host_sex",
    "submitted_host_sex",
    "host_body_site",
    "host_gravidity",
    "host_phenotype",
    "host_genotype",
    "host_growth_conditions",
    "environmental_package",
    "investigation_type",
    "experimental_factor",
    "sample_collection",
    "sequencing_method",
    "target_gene",
    "ph",
    "sample_title",
    "sample_material",
    "taxonomic_identity_marker",
    "assembly_quality",
    "assembly_software",
    "taxonomic_classification",
    "completeness_score",
    "contamination_score",
    "binning_software",
    "lat",
    "lon",
    "sample_capture_status",
    "collection_date_submitted",
    "submission_tool",
]

# all available fields for taxonomic ID metadata query
# https://www.ebi.ac.uk/ena/portal/api/returnFields?query=tax_tree()&result=read_run
all_fields = [
    "study_accession",
    "secondary_study_accession",
    "sample_accession",
    "secondary_sample_accession",
    "experiment_accession",
    "run_accession",
    "submission_accession",
    "tax_id",
    "scientific_name",
    "instrument_platform",
    "instrument_model",
    "library_name",
    "library_layout",
    "nominal_length",
    "library_strategy",
    "library_source",
    "library_selection",
    "read_count",
    "base_count",
    "center_name",
    "first_public",
    "last_updated",
    "experiment_title",
    "study_title",
    "study_alias",
    "experiment_alias",
    "run_alias",
    "fastq_bytes",
    "fastq_md5",
    "fastq_ftp",
    "fastq_aspera",
    "fastq_galaxy",
    "submitted_bytes",
    "submitted_md5",
    "submitted_ftp",
    "submitted_aspera",
    "submitted_galaxy",
    "submitted_format",
    "sra_bytes",
    "sra_md5",
    "sra_ftp",
    "sra_aspera",
    "sra_galaxy",
    "cram_index_ftp",
    "cram_index_aspera",
    "cram_index_galaxy",
    "sample_alias",
    "broker_name",
    "nominal_sdev",
    "first_created",
    "sample_description",
    "parent_study",
    "library_construction_protocol",
    "accession",
    "bio_material",
    "cell_line",
    "cell_type",
    "collected_by",
    "collection_date",
    "country",
    "cultivar",
    "culture_collection",
    "description",
    "dev_stage",
    "ecotype",
    "environmental_sample",
    "germline",
    "identified_by",
    "isolate",
    "isolation_source",
    "location",
    "mating_type",
    "serotype",
    "serovar",
    "sex",
    "submitted_sex",
    "specimen_voucher",
    "strain",
    "sub_species",
    "sub_strain",
    "tissue_lib",
    "tissue_type",
    "variety",
    "checklist",
    "depth",
    "elevation",
    "altitude",
    "environment_biome",
    "environment_feature",
    "environment_material",
    "temperature",
    "salinity",
    "sampling_campaign",
    "sampling_site",
    "sampling_platform",
    "protocol_label",
    "project_name",
    "host",
    "host_tax_id",
    "host_status",
    "host_sex",
    "submitted_host_sex",
    "host_body_site",
    "host_gravidity",
    "host_phenotype",
    "host_genotype",
    "host_growth_conditions",
    "environmental_package",
    "investigation_type",
    "experimental_factor",
    "sample_collection",
    "sequencing_method",
    "target_gene",
    "ph",
    "sample_title",
    "sample_material",
    "taxonomic_identity_marker",
    "assembly_quality",
    "assembly_software",
    "taxonomic_classification",
    "completeness_score",
    "contamination_score",
    "binning_software",
    "lat",
    "lon",
    "sample_capture_status",
    "collection_date_submitted",
    "submission_tool",
]


def get_taxon_metadata(
    taxon_id,
    file_type="JSON",
    fields=original_fields,
    instrument_platform="illumina",
    library_source="TRANSCRIPTOMIC",
    limit=0,
):
    """
    API endpoint docs:
    https://www.ebi.ac.uk/ena/portal/api/#/Portal%20API/searchUsingGET
    """
    base_url = "https://www.ebi.ac.uk/ena/portal/api/search"

    parameters = {
        "query": f"tax_tree({taxon_id})",
        "result": "read_run",
        "format": file_type,
        "instrument_platform": instrument_platform,
        "library_source": library_source,
        "limit": limit,
        "fields": str.join(",", fields),
    }

    response = requests.get(base_url, params=parameters)
    response.raise_for_status()

    return response.content


def save_taxon_metadata(taxon_id, file_type="JSON", fields=original_fields):
    """
    """
    taxon_metadata = get_taxon_metadata(taxon_id, file_type=file_type, fields=fields)

    taxon_metadata_path = f"taxon_id={taxon_id}.json"
    with open(taxon_metadata_path, "wb+") as file:
        file.write(taxon_metadata)


def main():
    """
    main function
    """
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        "--taxon_id",
        type=str,
        help="taxonomic ID",
    )
    argument_parser.add_argument(
        "--file_type",
        type=str,
        default="JSON",
        help="output file type",
    )

    args = argument_parser.parse_args()

    # download taxon_id metadata
    if args.taxon_id:
        # fields = original_fields
        # fields = original_fields + additional_fields
        fields = original_fields + additional_fields + remaining_fields
        # fields = all_fields
        save_taxon_metadata(args.taxon_id, file_type=args.file_type, fields=fields)

    else:
        argument_parser.print_help()
        sys.exit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted with CTRL-C, exiting...")
