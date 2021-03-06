# OpenFF BCC Refit Study COH v2.0

### Description

A data set curated for the initial stage of the on-going OpenFF study which aims to co-optimize the AM1BCC bond charge correction (BCC) parameters against an experimental training set of density and enthalpy of mixing data points and a QM training set of electric field data.
    
The initial data set is limited to only molecules composed of C, O, H. This limited scope significantly reduces the number of BCC parameters which must be retrained, thus allowing for easier convergence of the initial optimizations.

The included molecules were combinatorially generated to cover a range of alcohol, ether, and carbonyl containing molecules.

### General Information

- Date: 2021.06.22
- Class: OpenFF Optimization Dataset
- Purpose: C,H,O training data for BCC refits.
- Collection: OptimizationDataset
- Name: OpenFF BCC Refit Study COH v2.0
- Number of unique molecules        200
- Number of filtered molecules      0
- Number of conformers              1550
- Number of conformers min mean max 1   7.75 10
- Dataset Submitter: Simon Boothroyd
- Dataset Generator: Simon Boothroyd
- Set of charges: [0.0]
- Mean molecular weight: 117.62
- Max molecular weight: 204.31
- Enumerate stereoisomers: False
- Enumerate tautomers: False
- Enumerate protomers: False

### QCSubmit generation pipeline

- `generate-dataset.ipynb`: A notebook which shows how the dataset was prepared from the input files.
- `generate-smiles.py`: A python script which combines an aniline scaffold with diverse functional groups. 

### QCSubmit Manifest

- `generate-dataset.ipynb`
- `generate-smiles.py`
- `dataset.json.bz2`: The basic dataset ready for submission.
- `dataset.pdf`: A pdf file containing molecule 2D structures.
- `dataset.smi`: SMILES for every molecule in the submission.
 
### Metadata

```
{'collection_type': 'OptimizationDataset',
 'creation_date': datetime.date(2021, 7, 2),
 'dataset_name': 'OpenFF BCC Refit Study COH v2.0',
 'elements': {'H', 'O', 'C'},
 'long_description': 'A data set curated for the initial stage of the on-going '
                     'OpenFF study which aims to co-optimize the AM1BCC bond '
                     'charge correction (BCC) parameters against an '
                     'experimental training set of density and enthalpy of '
                     'mixing data points and a QM training set of electric '
                     'field data.\n'
                     '\n'
                     'The initial data set is limited to only molecules '
                     'composed of C, O, H. This limited scope significantly '
                     'reduces the number of BCC parameters which must be '
                     'retrained, thus allowing for easier convergence of the '
                     'initial optimizations.\n'
                     '\n'
                     'The included molecules were combinatorially generated to '
                     'cover a range of alcohol, ether, and carbonyl containing '
                     'molecules.',
 'long_description_url': HttpUrl('https://github.com/openforcefield/qca-dataset-submission/tree/master/submissions/2021-06-22-OpenFF-BCC-Refit-Study-COH-v2.0', scheme='https', host='github.com', tld='com', host_type='domain', path='/openforcefield/qca-dataset-submission/tree/master/submissions/2021-06-22-OpenFF-BCC-Refit-Study-COH-v2.0'),
 'short_description': 'Optimizations of diverse, para-substituted aniline '
                      'derivatives.',
 'submitter': 'simonboothroyd'}
```

## QC specifications:

```
Spec: hf/6-31G*
{'basis': '6-31G*',
 'implicit_solvent': None,
 'keywords': None,
 'method': 'hf',
 'program': 'psi4',
 'spec_description': 'The quantum chemistry specification used to generate the '
                     'original AM1BCCs.',
 'spec_name': 'hf/6-31G*',
 'store_wavefunction': 'orbitals_and_eigenvalues'}
Spec: pw6b95/aug-cc-pV(D+d)Z/uf
{'basis': 'aug-cc-pV(D+d)Z',
 'implicit_solvent': None,
 'keywords': {'dft_pruning_scheme': 'robust',
              'dft_radial_points': 99,
              'dft_spherical_points': 590},
 'method': 'pw6b95',
 'program': 'psi4',
 'spec_description': 'The quantum chemistry specification used in the RESP2 '
                     'publication for the vacuum (i.e. no PCM) calculations '
                     "modified to use an 'ultra-fine' DFT grid to improve SCF "
                     'convergence.',
 'spec_name': 'pw6b95/aug-cc-pV(D+d)Z/uf',
 'store_wavefunction': 'orbitals_and_eigenvalues'}
Spec: pw6b95/aug-cc-pV(D+d)Z/uf,pcm
{'basis': 'aug-cc-pV(D+d)Z',
 'implicit_solvent': {'cavity_Area': 0.3,
                      'cavity_MinRadius': 52.917721067,
                      'cavity_Mode': 'Implicit',
                      'cavity_RadiiSet': 'Bondi',
                      'cavity_Scaling': True,
                      'cavity_Type': 'GePol',
                      'codata': 2010,
                      'medium_Correction': 0.0,
                      'medium_DiagonalScaling': 1.07,
                      'medium_MatrixSymm': True,
                      'medium_Nonequilibrium': False,
                      'medium_ProbeRadius': 0.52917721067,
                      'medium_Solvent': 'H2O',
                      'medium_SolverType': 'CPCM',
                      'units': 'angstrom'},
 'keywords': {'dft_pruning_scheme': 'robust',
              'dft_radial_points': 99,
              'dft_spherical_points': 590},
 'method': 'pw6b95',
 'program': 'psi4',
 'spec_description': 'The quantum chemistry specification used in the RESP2 '
                     'publication for the aqueous (i.e. with PCM) calculations '
                     "modified to use an 'ultra-fine' DFT grid to improve SCF "
                     'convergence.',
 'spec_name': 'pw6b95/aug-cc-pV(D+d)Z/uf,pcm',
 'store_wavefunction': 'orbitals_and_eigenvalues'}
```

## SCF Properties

```
[<SCFProperties.Dipole: 'dipole'>,
 <SCFProperties.Quadrupole: 'quadrupole'>,
 <SCFProperties.WibergLowdinIndices: 'wiberg_lowdin_indices'>,
 <SCFProperties.MayerIndices: 'mayer_indices'>]
```
