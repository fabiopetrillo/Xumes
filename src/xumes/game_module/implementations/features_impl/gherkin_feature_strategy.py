import os
from typing import Dict

from gherkin.parser import Parser
from gherkin.token_scanner import TokenScanner

from xumes.game_module.feature_strategy import FeatureStrategy, Feature, Scenario


class GherkinFeatureStrategy(FeatureStrategy):

    def __init__(self, alpha: float = 0.001):
        super().__init__(alpha)
        self._steps = []

    def retrieve_feature(self):
        """
        Get features and scenarios from every feature file ".feature" in the "./features" directory.
        """

        # Convert steps files to list of gherkin steps
        self._convert_steps_files_to_gherkin_steps()

        # Get all feature files
        feature_files = os.listdir("./features")

        # If there is no feature files, raise an exception
        if len(feature_files) == 0:
            raise Exception("Feature files not found.")

        # Initialize parser
        parser = Parser()

        # Iterate over feature files
        for feature_file in feature_files:

            # We open the feature file and compile him
            path = os.path.join("./features", feature_file)
            with open(path, 'r') as file:
                feature = parser.parse(TokenScanner(file.read()))['feature']

                # We create a Feature object
                feature_obj = Feature(name=feature_file[:-8])

                # We iterate over every scenario in the feature file
                for scenario in feature['children']:
                    scenario = scenario['scenario']
                    # Find the steps file for the scenario using pattern matching
                    steps_file, given_params, when_params, then_params = self._find_steps_file(scenario)

                    # Fill parameters
                    self.given.all[steps_file]['params'] = given_params
                    self.when.all[steps_file]['params'] = when_params
                    self.then.all[steps_file]['params'] = then_params

                    # We create a Scenario object
                    scenario_obj = Scenario(scenario['name'], steps_file, feature_obj)
                    feature_obj.scenarios.append(scenario_obj)

                # We append the feature to the list of features
                self.features.append(feature_obj)

    def _convert_steps_files_to_gherkin_steps(self):
        self._steps.clear()
        for name in self.given.all:
            try:
                given = self.given.all[name]
            except IndexError:
                raise Exception("Given steps not found.")
            try:
                when = self.when.all[name]
            except IndexError:
                raise Exception("When steps not found.")
            try:
                then = self.then.all[name]
            except IndexError:
                raise Exception("Then steps not found.")

            given_name = given['content']
            when_name = when['content']
            then_name = then['content']

            self._steps.append({
                "name": name,
                "given": given_name,
                "when": when_name,
                "then": then_name
            })

    def _find_steps_file(self, scenario: Dict):
        """
        Find the steps file for the scenario using pattern matching.
        """
        # Get scenario name
        scenario_given = scenario['steps'][0]['text']
        scenario_when = scenario['steps'][1]['text']
        scenario_then = scenario['steps'][2]['text']

        # Iterate over steps files
        for steps_file in self._steps:
            # Get steps file name
            steps_file_name = steps_file['name']
            steps_file_given = steps_file['given']
            steps_file_when = steps_file['when']
            steps_file_then = steps_file['then']

            # Check if the scenario name corresponds to the steps file name
            given_parameters = self._pattern_matching(steps_file_given, scenario_given)
            when_parameters = self._pattern_matching(steps_file_when, scenario_when)
            then_parameters = self._pattern_matching(steps_file_then, scenario_then)

            if given_parameters != False and when_parameters != False and then_parameters != False:
                return steps_file_name, given_parameters, when_parameters, then_parameters
        # If no steps file was found, raise an exception
        raise Exception("Steps file not found.")

    @staticmethod
    def _pattern_matching(step: str, scenario: str):
        # Check if the step str corresponds to the scenario str
        # And return parameters if it does

        # Split step and scenario
        step = step.split(" ")
        scenario = scenario.split(" ")

        # If the length of the step is different from the length of the scenario, return False
        if len(step) != len(scenario):
            return False

        # Iterate over step and scenario
        parameters = {}
        for i in range(len(step)):
            # If the step and scenario are different, return False
            if step[i] != scenario[i]:
                # If the step is not a parameter, return False
                if step[i][0] != "{" or step[i][-1] != "}":
                    return False
                # If the step is a parameter, append the parameter to the list of parameters
                parameters[step[i][1:-1]] = scenario[i]

        # If the step and scenario are equal, return the parameters
        return parameters
