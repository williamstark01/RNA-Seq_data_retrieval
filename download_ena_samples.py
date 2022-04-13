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


def get_taxon_metadata(
    taxon_id,
    instrument_platform="illumina",
    library_source="TRANSCRIPTOMIC",
    limit=0,
):
    """
    """
    base_url = "https://www.ebi.ac.uk/ena/portal/api/search"

    fields = [
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

    parameters = {
        "query": f"tax_tree({taxon_id})",
        "result": "read_run",
        "format": "JSON",
        "instrument_platform": instrument_platform,
        "library_source": library_source,
        "limit": limit,
        "fields": str.join(",", fields),
    }

    response = requests.get(base_url, params=parameters)
    response.raise_for_status()

    return response.content


def save_taxon_metadata(taxon_id):
    """
    """
    taxon_metadata = get_taxon_metadata(taxon_id)

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
        help="taxonomic ID"
    )

    args = argument_parser.parse_args()

    # download taxon_id metadata
    if args.taxon_id:
        save_taxon_metadata(args.taxon_id)

    else:
        argument_parser.print_help()
        sys.exit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted with CTRL-C, exiting...")
