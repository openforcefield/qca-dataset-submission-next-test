<!-- Choose the checklist below based on the type of PR this is -->
<!-- Delete all other checklists -->


## New Submission Checklist

- [ ] Created a new folder in the submissions directory containing the dataset
- [ ] Added `README.md` describing the dataset see [here](https://github.com/openforcefield/qca-dataset-submission/tree/master/submissions/2020-03-26-OpenFF-Gen-2-Torsion-Set-6-supplemental-2) for examples
- [ ] All files used to produce the dataset are included with a description
- [ ] Dataset follows the QCSubmit schema defined for [Datasets](https://github.com/openforcefield/qcsubmit/blob/56680a7d3298b5d8962edcb840b0fdb34558c053/qcsubmit/datasets.py#L340), [OptimizationDatasets](https://github.com/openforcefield/qcsubmit/blob/56680a7d3298b5d8962edcb840b0fdb34558c053/qcsubmit/datasets.py#L1062) and [TorsionDriveDatasets](https://github.com/openforcefield/qcsubmit/blob/56680a7d3298b5d8962edcb840b0fdb34558c053/qcsubmit/datasets.py#L1225)
- [ ] Dataset filename matches pattern `dataset*.json`; may feature a compression extension, such as `.bz2`
- [ ] A PDF depicting the molecules is attached, in the case of torsiondrives this should include the highlighting of the central bond, this can be done automatically using [qcsubmit](https://github.com/openforcefield/qcsubmit/blob/56680a7d3298b5d8962edcb840b0fdb34558c053/qcsubmit/datasets.py#L854). 
- [ ] QCSubmit validation passed
- [ ] Made a new dataset entry in the mapping table in repository `README.md`
- [ ] Ready to submit!


## Compute Expansion Checklist

- [ ] Compute expansion filename matches pattern `compute*.json`; may feature a compression extension, such as `.bz2`
- [ ] QCSubmit validation passed
- [ ] Ready to submit!
