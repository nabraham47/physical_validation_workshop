# Full documentation at http://physical-validation.readthedocs.io/
import physical_validation as pv

# Create a flat file parser
parser = pv.data.FlatfileParser()

# Our test system consists of 900 H2O molecules whose bonds are fully constrained.
# During the simulation, we kept the translation of the center of mass to zero,
# so we need to reduce the number of degrees of freedom by 3.
system = pv.data.SystemData(
    natoms=900*3,
    nconstraints=900*3,
    ndof_reduction_tra=3,
    ndof_reduction_rot=0
)

# The physical validation tests need some information on the units that were used
# in the simulation. While the strings are only used for output, the conversion
# respective to GROMACS units are relevant for the calculations. Please see the
# documentation for more information.
units = pv.data.UnitData(
    kb=8.314462435405199e-3,
    energy_str='kJ/mol',
    energy_conversion=1.0,
    length_str='nm',
    length_conversion=1.0,
    volume_str='nm^3',
    volume_conversion=1.0,
    temperature_str='K',
    temperature_conversion=1.0,
    pressure_str='bar',
    pressure_conversion=1.0,
    time_str='ps',
    time_conversion=1.0
)

# For the flat file example, we will only look at the simulations performed under
# NVT conditions using the velocity-rescale thermostat. There are two simulations:
# One ran at 300K, and one ran at 308K.
ensemble_1 = pv.data.EnsembleData(
    ensemble='NVT',
    natoms=900*3,
    volume=3.01125**3,
    temperature=300
)
ensemble_2 = pv.data.EnsembleData(
    ensemble='NVT',
    natoms=900*3,
    volume=3.01125**3,
    temperature=308
)
dir_1 = 'md_NVT_vr_1'
dir_2 = 'md_NVT_vr_2'

# We can now read in our flat data files (1-dimensional ascii files containing
# energy trajectories), and create a simulation result representation usable by
# the physical validation tests.
result_1 = parser.get_simulation_data(
    units=units, ensemble=ensemble_1, system=system,
    kinetic_ene_file=dir_1 + '/kinetic_energy.dat',
    potential_ene_file=dir_1 + '/potential_energy.dat',
    total_ene_file=dir_1 + '/total_energy.dat'
)
result_2 = parser.get_simulation_data(
    units=units, ensemble=ensemble_2, system=system,
    kinetic_ene_file=dir_2 + '/kinetic_energy.dat',
    potential_ene_file=dir_2 + '/potential_energy.dat',
    total_ene_file=dir_2 + '/total_energy.dat'
)

# As with the other parsers, we can now test, for example, the kinetic energy using the
# created simulation result data structure, where
# the first input is the simulation results read in,
# `strict` determines whether we test the full distribution (True)
# or only determine the mean and the variance of the distribution (False),
# `verbosity` sets the level of detail of the output  (with verbosity=0
# being quiet and verbosity=3 being the most chatty), and the filename is being used to
# plot the resulting distribution for visual inspection.
print('==> Kinetic energy test of simulation ' + dir_1)
pv.kinetic_energy.distribution(result_1, strict=False, verbosity=2,
                               filename='ke_flat_vr_NVT_1')
print('==> Kinetic energy test of simulation ' + dir_2)
pv.kinetic_energy.distribution(result_2, strict=False, verbosity=2,
                               filename='ke_flat_vr_NVT_2')

# We can also test the distribution of the potential energy. While the first two
# inputs to the tests are the parsed simulation results, `verbosity` sets the level of
# detail of the output  (with verbosity=0 being quiet and verbosity=3 being the most chatty),
# and the filename is being used to plot the resulting distribution for visual inspection.
print('==> Potential energy test')
pv.ensemble.check(result_1, result_2,
                  verbosity=2, filename='pe_flat_vr_NVT')
