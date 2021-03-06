#!/usr/bin/env python

"""
Generate a PDF of all small molecules in the dataset.
"""

import gzip
from openeye import oechem

# Highlight element of interest
#subs = oechem.OESubSearch("[#5]") # boron
subs = None


ifile = oechem.oemolistream('pubLigsChargedGoodDensity.sdf')

# Build OEMols
oemols = list()
oemol = oechem.OEMol()
#for smiles in smiles_list:
while oechem.OEReadMolecule(ifile, oemol):
    #oechem.OESmilesToMol(oemol, smiles)
    oemols.append(oemol)
    oemol = oechem.OEMol()
ifile.close()

# Generate a PDF of all molecules in the set
pdf_filename = 'pubLigsChargedGoodDensity.pdf'

from openeye import oedepict
itf = oechem.OEInterface()
PageByPage = True
suppress_h = True
rows = 10
cols = 6
ropts = oedepict.OEReportOptions(rows, cols)
ropts.SetHeaderHeight(25)
ropts.SetFooterHeight(25)
ropts.SetCellGap(2)
ropts.SetPageMargins(10)
report = oedepict.OEReport(ropts)
cellwidth, cellheight = report.GetCellWidth(), report.GetCellHeight()
opts = oedepict.OE2DMolDisplayOptions(cellwidth, cellheight, oedepict.OEScale_Default * 0.5)
opts.SetAromaticStyle(oedepict.OEAromaticStyle_Circle)
pen = oedepict.OEPen(oechem.OEBlack, oechem.OEBlack, oedepict.OEFill_On, 1.0)
opts.SetDefaultBondPen(pen)
oedepict.OESetup2DMolDisplayOptions(opts, itf)
for i, mol in enumerate(oemols):
    cell = report.NewCell()
    mol_copy = oechem.OEMol(mol)
    oedepict.OEPrepareDepiction(mol_copy, False, suppress_h)
    disp = oedepict.OE2DMolDisplay(mol_copy, opts)

    # Highlight element of interest
    unique = False
    if subs is not None:
        for match in subs.Match(mol_copy, unique):
            oedepict.OEAddHighlighting(disp, oechem.OEColor(oechem.OEYellow), oedepict.OEHighlightStyle_BallAndStick, match)

    oedepict.OERenderMolecule(cell, disp)

oedepict.OEWriteReport(pdf_filename, report)
