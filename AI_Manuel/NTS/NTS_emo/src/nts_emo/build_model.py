"""
Build the pydae compiled library for the NTS two-machine system.

The Builder compiles the symbolic DAE into C code and then into a CFFI
shared library.  This step only needs to run once; subsequent runs reuse
the cached library unless force_rebuild=True.
"""

import json
import logging
import os
import sys


def build_nts_model(output_dir: str = './build',
                    force_rebuild: bool = False,
                    sparse: bool = False,
                    target: str = 'ctypes') -> str:
    """
    Build (or reload) the pydae compiled model for 'nts2gen'.

    Parameters
    ----------
    output_dir    : directory where the compiled library and JSON will be written
    force_rebuild : if True, always recompile even if the library exists
    sparse        : if True use KLU sparse solver; False uses dense LU (safer on Windows)
    target        : 'ctypes' (default, no MSVC needed) or 'cffi' (needs MSVC on Windows)

    Returns
    -------
    str — model name ('nts2gen')
    """
    from nts_emo.assembly import assemble_system

    os.makedirs(output_dir, exist_ok=True)
    abs_dir = os.path.abspath(output_dir)

    model_name = 'nts2gen'
    json_path  = os.path.join(abs_dir, f'{model_name}_data.json')

    if os.path.exists(json_path) and not force_rebuild:
        logging.info(f'[build_nts_model] Library already exists at {abs_dir}. '
                     'Pass force_rebuild=True to recompile.')
        return model_name

    # Import Builder directly (bypass pydae.core.__init__ which imports casadi)
    from pydae.core.builder.sympy_builder import Builder

    sys_dict = assemble_system()

    # Log variable counts
    Nx  = len(sys_dict['x_list'])
    Ny  = len(sys_dict['y_ini_list'])
    Nf  = len(sys_dict['f_list'])
    Ng  = len(sys_dict['g_list'])
    logging.info(f'[build_nts_model] System: {Nx} states, {Ny} algebraic vars, '
                 f'{Nf} ODEs, {Ng} algebraic eqs')

    if Nf != Nx:
        raise ValueError(f'Mismatch: {Nx} states but {Nf} differential equations')
    if Ng != Ny:
        raise ValueError(f'Mismatch: {Ny} algebraic vars but {Ng} algebraic equations')

    # Change to output directory so Builder writes files there
    orig_dir = os.getcwd()
    os.chdir(abs_dir)
    try:
        builder = Builder(sys_dict, target=target, sparse=sparse, verbose=True)
        builder.build()
    finally:
        os.chdir(orig_dir)

    logging.info(f'[build_nts_model] Build complete → {abs_dir}')
    return model_name


def load_model(model_dir: str = './build'):
    """
    Load the compiled 'nts2gen' model for use with pydae.ssa.

    Parameters
    ----------
    model_dir : directory containing nts2gen_data.json and the CFFI module

    Returns
    -------
    pydae Model instance (ready for .ini() calls)
    """
    from pydae.core.model.ctypes_model import Model

    abs_dir = os.path.abspath(model_dir)
    return Model('nts2gen', matrices_folder=abs_dir, data_folder=abs_dir)
