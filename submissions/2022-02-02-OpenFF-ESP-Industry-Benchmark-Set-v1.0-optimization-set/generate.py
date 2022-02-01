import logging
from multiprocessing import Pool
from typing import Optional, Tuple

from openff.qcsubmit.datasets import OptimizationDataset
from openff.qcsubmit.factories import OptimizationDatasetFactory
from openff.toolkit.topology import Molecule
from openff.toolkit.utils import OpenEyeToolkitWrapper, ToolkitRegistry
from openmm import unit
from qcelemental.models.results import WavefunctionProtocolEnum
from tqdm import tqdm


def generate_elf_conformers(smiles: str) -> Tuple[str, Optional[Molecule]]:

    toolkit_registry = ToolkitRegistry([OpenEyeToolkitWrapper()])

    molecule = Molecule.from_smiles(
        smiles,
        allow_undefined_stereo=True,
        toolkit_registry=toolkit_registry
    )

    try:
        molecule.generate_conformers(
            n_conformers=500,
            rms_cutoff=0.5 * unit.angstrom,
            toolkit_registry=toolkit_registry,
        )
        molecule.apply_elf_conformer_selection(toolkit_registry=toolkit_registry)
    except:
        logging.exception(f"failed to process {smiles}")
        return smiles, None

    return smiles, molecule


def main():

    # Generate the data set to submit. We build a dataset directly as the unique
    # checks fail at the isomorphism check stage...
    dataset_factory = OptimizationDatasetFactory()

    dataset = OptimizationDataset(
        dataset_name="OpenFF ESP Industry Benchmark Set v1.0",
        dataset_tagline="HF/6-31G* conformers of public industry benchmark molecules.",
        description="A dataset containing molecules from the `OpenFF Industry Benchmark "
        "Season 1 v1.1` molecule set with ELF conformers."
        "\n\n"
        "For each of the molecule, a set of up to five conformers were generated by:\n\n"
        "   * generating a set of up to 500 conformers with an RMS cutoff of 0.5 Å "
        "using the OpenEye backend of the OpenFF toolkit\n"
        "   * applying ELF conformer selection using the OpenEye backend of the OpenFF "
        "toolkit\n"
        "\n"
        "Each conformer will be converged according to the 'GAU_LOOSE' criteria."
    )
    dataset.clear_qcspecs()
    dataset.add_qc_spec(
        program="psi4",
        method="hf",
        basis="6-31G*",
        spec_name="HF/6-31G*",
        spec_description=(
            "The standard HF/6-31G* basis used to derive RESP style charges."
        ),
        store_wavefunction=WavefunctionProtocolEnum.orbitals_and_eigenvalues
    )

    with open("../2021-06-04-OpenFF-Industry-Benchmark-Season-1-v1.1/dataset.smi", "r") as file:
        smiles_set = [smiles for smiles in file.read().split("\n") if len(smiles) > 0]

    with Pool(processes=10) as pool:

        molecules = [
            (smiles, molecule)
            for smiles, molecule in tqdm(
                pool.imap(generate_elf_conformers, smiles_set), total=len(smiles_set)
            )
        ]

    for smiles, molecule in molecules:

        if molecule is None:
            print("skipping ", smiles)
            continue

        dataset.add_molecule(dataset_factory.create_index(molecule=molecule), molecule)

    # Correct the dataset metadata.
    dataset.metadata.submitter = "simonboothroyd"
    dataset.metadata.long_description_url = (
        "https://github.com/openforcefield/qca-dataset-submission/tree/master/"
        "submissions/"
        "2022-02-02-OpenFF-ESP-Industry-Benchmark-Set-v1.0"
    )

    # Export the data set.
    dataset.export_dataset("dataset.json.xz")
    dataset.molecules_to_file('dataset.smi', 'smi')

    dataset.visualize("dataset.pdf", columns=8)

    print(dataset.qc_specifications)

    print("N MOLECULES", dataset.n_molecules)
    print("N RECORDS", dataset.n_records)


if __name__ == '__main__':
    main()
