#!/usr/bin/env python3

import yaml
import os

config_file = os.environ["INPUT_CONFIG_FILE"]

with open(f"/github/workspace/{config_file}", "r") as stream:
    config = yaml.safe_load(stream)

env = os.getenv("APP_ENV")
if env is None:
    # Use the first part of the branch name to ensure feature and hotfix
    # branches just return feature or hotfix.
    env = os.environ["GITHUB_REF"].replace("refs/heads/", "").split("/")[0]

defaultConfig = config.get("default", {})
envConfig = config.get(env)

if not isinstance(defaultConfig, dict):
    raise Exception("Default config is not an instance of dictionary")

if not envConfig or not isinstance(envConfig, dict):
    print(f"No config explicitly defined for environment {env}, using default")
    envConfig = {}

mergedConfig = {**defaultConfig, **envConfig}

with open(os.environ["GITHUB_ENV"], "a") as environment_file:

    for k, v in mergedConfig.items():
        if "\n" in str(v):
            environment_file.write(f"{k.upper()}<<delimiter\n{v}delimiter\n")
        else:
            environment_file.write(f"{k.upper()}={v}\n")

    owner_length = len(os.environ["GITHUB_REPOSITORY_OWNER"]) + 1
    repo_name = os.environ["GITHUB_REPOSITORY"][owner_length:]

    environment_file.write(f"APP_ENV={env}\n")
    environment_file.write(f"REPO_NAME={repo_name}\n")
    environment_file.write(f"REPO_NAME_DASH={repo_name.replace('.','-')}\n")
