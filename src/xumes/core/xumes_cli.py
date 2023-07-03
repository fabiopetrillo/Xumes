import logging
import os

import click

from xumes.game_module.implementations.rest_impl.communication_service_test_manager_rest_api import \
    CommunicationServiceTestManagerRestApi
from xumes.game_module.test_manager import PygameTestManager, TEST_MODE, TRAIN_MODE, RENDER_MODE
from xumes.training_module.implementations.rest_impl.communication_service_trainer_manager_rest_api import \
    CommunicationServiceTrainerManagerRestApi
from xumes.training_module.trainer_manager import FEATURE_MODE, SCENARIO_MODE, VecStableBaselinesTrainerManager, \
    StableBaselinesTrainerManager


@click.group()
def cli():
    pass


def get_debug_level(debug):
    if debug:
        return logging.DEBUG
    return logging.INFO


@cli.command()
@click.option("--render", is_flag=True, help="Render the game.")
@click.option("--test", is_flag=True, help="Test the game.")
@click.option("--train", is_flag=True, help="Train the game.")
@click.option("--timesteps", "-t", default=None, help="Number of timesteps to test the game.")
@click.option("--iterations", "-i", default=None, help="Number of iterations to test the game.")
@click.option("--debug", is_flag=True, help="Debug the game.")
@click.option("--ip", default="localhost", help="IP of the training server.")
@click.option("--port", default=5000, help="Port of the training server.")
@click.option("--path", default=None, type=click.Path(), help="Path of the trainers.")
def tester(train, debug, render, test, ip, port, path, timesteps, iterations):

    if path:
        os.chdir(path)
    else:
        print("You must choose a path to save the model.")
        return

    if not train and not test:
        print("You must choose between --train or --test.")
        return

    if test and not timesteps and not iterations:
        print("You must choose a number of timesteps or iterations to test the game.")
        return

    logging.basicConfig(format='%(levelname)s:%(message)s', level=get_debug_level(debug))

    if train:
        mode = TRAIN_MODE
    else:
        mode = TEST_MODE
    if render:
        mode = RENDER_MODE

    if timesteps:
        timesteps = int(timesteps)

    if iterations:
        iterations = int(iterations)

    test_manager = PygameTestManager(communication_service=CommunicationServiceTestManagerRestApi(ip=ip, port=port),
                                     mode=mode, timesteps=timesteps, iterations=iterations)
    test_manager.test_all()


@cli.command()
@click.option("--test", is_flag=True, help="Test the game.")
@click.option("--train", is_flag=True, help="Train the agent.")
@click.option("--mode", default=FEATURE_MODE, help="Mode of the training. (scenario, feature=default)")
@click.option("--debug", is_flag=True, help="Debug the trainer.")
@click.option("--port", default=5000, help="Port of the training server.")
@click.option("--path", default=None, type=click.Path(), help="Path of the tests folder.")
def trainer(train, debug, test, path, mode, port,):

    if path:
        os.chdir(path)
    else:
        print("You must choose a path to save the model.")
        return

    logging.basicConfig(format='%(levelname)s:%(message)s', level=get_debug_level(debug))

    if not train and not test:
        print("You must choose between --train or --test.")
        return

    if mode == "scenario":
        model_mode = SCENARIO_MODE
    else:
        model_mode = FEATURE_MODE

    if train:
        mode = TRAIN_MODE
    else:
        mode = TEST_MODE

    if model_mode == FEATURE_MODE:
        training_manager = VecStableBaselinesTrainerManager(CommunicationServiceTrainerManagerRestApi(), port)
        training_manager.run()
        if mode == TRAIN_MODE:
            training_manager.train()
        else:
            training_manager.play()
    elif model_mode == SCENARIO_MODE:
        training_manager = StableBaselinesTrainerManager(CommunicationServiceTrainerManagerRestApi(), mode=mode)
        training_manager.run()


if __name__ == '__main__':
    cli()
