# Quantum Chemistry Benchmarking Pipeline for Molecular HER Electrocatalysts

This repository contains the automation scripts and computational workflows used to establish baseline electronic and structural parameters for benchmark hydrogen evolution reaction (HER) electrocatalysts, specifically targeting the seminal DuBois-type nickel bis-diphosphine complexes ($[Ni(P^R_2N^{R'}_2)_2]^{2+}$).

## Module Overview: `run_tmqm_orca_only.py`

The `run_tmqm_orca_only.py` script provides an automated, space-safe execution pipeline designed to interface with the **ORCA Quantum Chemistry Package**. It automates the extraction of single-point electronic properties mapped to the methodology of the tmQM dataset, bypassing standard pathing limitations on Windows operating systems.

### Workflow Stages

1. **File Parsing:** Validates the integrity of input `.xyz` coordinates derived from crystallographic data (e.g., Cambridge Structural Database / Mercury).
2. **Dynamic Input Generation:** Automatically formats high-precision inputs using Density Functional Theory (DFT) at the `TPSSh-D3BJ/def2-SVP` level of theory. It applies the `RIJCOSX` approximation with an auxiliary basis set (`def2/J`) and integration grid (`DefGrid2`) to accelerate calculations without compromising accuracy.
3. **Execution Routing:** Employs absolute pathing to prevent standard Windows command-line terminal errors when calling the ORCA executable.
4. **Automated Property Extraction:** Programmatically parses output `.out` files via regex to extract and log critical descriptors:
   * **Highest Occupied Molecular Orbital (HOMO)** energy (eV)
   * **Lowest Unoccupied Molecular Orbital (LUMO)** energy (eV)
   * **HOMO-LUMO Gap (HL Gap)** ($E_{LUMO} - E_{HOMO}$) (eV)
   * **Total Dipole Moment** (Debye)

### Prerequisites & Requirements

* **ORCA Software Package** (v6.1.1 or higher) installed locally.
* **Python 3.10+** with standard libraries (`subprocess`, `re`, `logging`, `datetime`).
* An active working directory completely **free of spaces** in the folder names (e.g., `C:\Catalyst_Run`) to ensure compatibility with ORCA's internal sub-routines.

### Usage

Place your target catalyst coordinates (`.xyz`) and the script into a space-free directory, update the absolute path to `orca.exe` on Line 12 of the script, and execute:

```bash
python run_tmqm_orca_only.py <catalyst_coordinates.xyz>