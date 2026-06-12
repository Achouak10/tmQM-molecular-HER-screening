import os
import subprocess
import re
import sys
import logging
import datetime

# ==========================================
# 1. DYNAMIC LOGGING & CONFIG
# ==========================================
# Ensure this is your exact, working, space-free path
ORCA_EXE = r"C:\ORCA_6.1.1\orca.exe"

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"pipeline_debug_{timestamp}.log"

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_filename, mode='w', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

def generate_orca_xtb_opt(xyz_filename):
    logging.info("--- Phase 1: ORCA Internal XTB2 Optimization ---")
    try:
        with open(xyz_filename, 'r') as f:
            lines = f.readlines()
        atom_count = int(lines[0].strip())
        coordinates = "".join(lines[2:2+atom_count])
    except Exception as e:
        logging.error(f"Failed to read {xyz_filename}: {e}")
        sys.exit(1)

    # Fast geometry optimization using the built-in XTB engine
    inp_content = f"""! XTB2 Opt
! NormalPrint

* xyz 2 1
{coordinates}*
"""
    inp_filename = "step1_xtb_opt.inp"
    with open(inp_filename, 'w') as f:
        f.write(inp_content)
    logging.info(">> Created step1_xtb_opt.inp")
    return inp_filename

def generate_orca_dft_sp(opt_xyz_filename):
    logging.info("--- Phase 2: ORCA TPSSh Single Point Calculation ---")
    try:
        with open(opt_xyz_filename, 'r') as f:
            lines = f.readlines()
        atom_count = int(lines[0].strip())
        coordinates = "".join(lines[2:2+atom_count])
    except Exception as e:
        logging.error(f"Failed to read {opt_xyz_filename}: {e}")
        sys.exit(1)

    # Pure Single Point Calculation (No 'Opt'). Takes minutes instead of days.
    inp_content = f"""! TPSSh def2-SVP D3BJ RIJCOSX def2/J DefGrid2
! NormalPrint

* xyz 2 1
{coordinates}*
"""
    inp_filename = "step2_dft_sp.inp"
    with open(inp_filename, 'w') as f:
        f.write(inp_content)
    logging.info(">> Created step2_dft_sp.inp")
    return inp_filename

def run_orca(inp_filename, out_filename):
    logging.info(f"Executing: {inp_filename}")
    cmd = f'"{ORCA_EXE}" {inp_filename} > {out_filename}'
    
    try:
        subprocess.run(cmd, shell=True, check=True)
        logging.info(f">> Job complete: {out_filename}")
    except subprocess.CalledProcessError as e:
        logging.error(f"ORCA CRASHED during {inp_filename}. Check {out_filename}.")
        sys.exit(1)
    return out_filename

def extract_properties(orca_out_filename):
    logging.info("--- Extracting Computational Results ---")
    homo, lumo, dipole = None, None, None
    
    try:
        with open(orca_out_filename, 'r') as f:
            content = f.read()
            
        orbital_matches = re.findall(r'\s*\d+\s+([0-2]\.\d+)\s+([-]?\d+\.\d+)\s+([-]?\d+\.\d+)', content)
        if orbital_matches:
            for i in range(len(orbital_matches) - 1):
                occ_current = float(orbital_matches[i][0])
                occ_next = float(orbital_matches[i+1][0])
                if occ_current > 0.0 and occ_next == 0.0:
                    homo = float(orbital_matches[i][2])
                    lumo = float(orbital_matches[i+1][2])
                    break

        dipole_match = re.search(r'Total Dipole Moment\s+:\s+([-]?\d+\.\d+)', content)
        if dipole_match:
            dipole = float(dipole_match.group(1))

        logging.info("\n==========================================")
        logging.info("           FINAL BASELINE VALUES          ")
        logging.info("==========================================")
        if homo is not None and lumo is not None:
            gap = lumo - homo
            logging.info(f"HOMO Energy:   {homo:.4f} eV")
            logging.info(f"LUMO Energy:   {lumo:.4f} eV")
            logging.info(f"HL Gap:        {gap:.4f} eV")
        else:
            logging.warning("Could not locate HOMO/LUMO.")

        if dipole is not None:
            logging.info(f"Dipole Moment: {dipole:.4f} D")
        else:
            logging.warning("Could not locate Dipole Moment.")
        logging.info("==========================================\n")
            
    except Exception as e:
        logging.error(f"Failed to extract properties: {str(e)}")

if __name__ == "__main__":
    logging.info("==========================================")
    logging.info(f"   STARTING ACCELERATED PIPELINE (Run: {timestamp})   ")
    logging.info("==========================================")
    
    if len(sys.argv) < 2:
        logging.error("Usage: python script.py <catalyst_coordinates.xyz>")
        sys.exit(1)
        
    initial_xyz = sys.argv[1]
    
    # Phase 1: Fast Geometry Opt
    xtb_inp = generate_orca_xtb_opt(initial_xyz)
    run_orca(xtb_inp, "step1_xtb_opt.out")
    
    # Phase 2: DFT Single Point
    dft_inp = generate_orca_dft_sp("step1_xtb_opt.xyz")
    run_orca(dft_inp, "step2_dft_sp.out")
    
    # Extract
    extract_properties("step2_dft_sp.out")