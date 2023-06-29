# Implementation of Kubeflow pipeline that say Hi to a person.
# Author: David Cardozo <david.cardozo@me.com>
from kfp.dsl import container_component, ContainerSpec, pipeline


@container_component
def say_hi_component(name: str):
    return ContainerSpec(
        image="python:3.11-alpine3.18",
        command=["python", "-c"],
        args=[f'print("Hi, {name}!")'],
    )


@container_component
def say_bye_component(name: str):
    return ContainerSpec(
        image="python:3.11-alpine3.18",
        command=["python", "-c"],
        args=[f'print("Bye, {name}!")'],
    )


@pipeline
def pipeline_to_say_hi(name_user: str = "David"):
    say_hi_task = say_hi_component(name=name_user)
    say_bye_task = say_bye_component(name=name_user).after(  # pylint: disable=no-member
        say_hi_task
    )


if __name__ == "__main__":
    import kfp.compiler as compiler
    from pathlib import Path

    compiler.Compiler().compile(pipeline_to_say_hi, "pipeline.yaml")
