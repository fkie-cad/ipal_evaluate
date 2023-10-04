import logging
from io import TextIOWrapper

version = "v1.2.7"

# Gzip options
compresslevel = 9  # 0 no compress, 1 large/fast, 9 small/slow

# In and output
input = None
inputfd: TextIOWrapper
output = None
outputfd: TextIOWrapper
attacks = None
timed_dataset = True

# Logging settings
logger = logging.getLogger("Evaluate")
log = logging.WARNING
logformat = "%(levelname)s:%(name)s: %(message)s"
logfile = "-"

# FPA grace time
alarm_gracetime = 0

# Metric settings
fscore_betas = [0.1, 0.5, 1, 2, 10]  # calculate the f1-score

# TaPR settings
eTaPR_theta_p = 0.5
eTaPR_theta_r = 0.01
eTaPR_delta = 0.0

# BATADAL settings
batadal_gamma = 0.5

# NAB-score settings.
nab_profile_default = {
    "nab_atp": 1,
    "nab_afp": -0.11,
    "nab_afn": -1,
}
nab_profile_low_fp = {
    "nab_atp": 1,
    "nab_afp": -0.22,
    "nab_afn": -1,
}
nab_profile_low_fn = {
    "nab_atp": 1,
    "nab_afp": -0.11,
    "nab_afn": -2.0,
}

nab_profiles = {
    "default": nab_profile_default,
    "reward_low_fp": nab_profile_low_fp,
    "reward_low_fn": nab_profile_low_fn,
}

# ipal-tune settings
config = None
configfile = None
restart = False
resume_errored = False
max_cpus = None
max_gpus = None


def evaluation_settings_to_dict():
    return {
        "version": version,
        # Generic settings
        "compresslevel": compresslevel,
        "input": input,
        "output": output,
        "attacks": attacks,
        "timed_dataset": timed_dataset,
        # Metric-specific settings
        "alarm_gracetime": alarm_gracetime,
        "fscore_beta": fscore_betas,
        "eTaPR_theta_p": eTaPR_theta_p,
        "eTaPR_theta_r": eTaPR_theta_r,
        "eTaPR_delta": eTaPR_delta,
        "batadal_gamma": batadal_gamma,
        "nab_profiles": nab_profiles,
        # Logging settings
        "log": log,
        "logformat": logformat,
        "logfile": logfile,
    }


def tuner_settings_to_dict():
    return {
        "version": version,
        # Generic settings
        "compresslevel": compresslevel,
        # Logging settings
        "log": log,
        "logformat": logformat,
        "logfile": logfile,
        # tune-specific settings
        "config_file": configfile,
        "restart": restart,
        "resume_errored": resume_errored,
        "max_cpus": max_cpus,
        "max_gpus": max_gpus,
    }
