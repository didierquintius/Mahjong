# -*- coding: utf-8 -*-

import itertools


class PointCalculator:
    def __init__(self, characters):
        self.allowed_configuration_pattern = {
            0: [],
            1: [],
            2: [[2]],
            3: [[3]],
            4: [[4]],
            5: [[2, 3]],
            6: [[3, 3], [2, 4]],
            7: [[4, 3]],
            8: [[4, 4], [2, 3, 3]],
            9: [[3, 3, 3], [2, 4, 3]],
            10: [[4, 3, 3], [2, 4, 4]],
            11: [[4, 4, 3], [2, 3, 3, 3]],
            12: [[3, 3, 3, 3], [4, 4, 4], [2, 4, 3, 3]],
            13: [[3, 3, 3, 4], [2, 4, 4, 3]],
            14: [[2, 3, 3, 3, 3], [4, 4, 3, 3], [2, 4, 4, 4]],
            15: [[4, 4, 4, 3], [2, 4, 3, 3, 3]],
            16: [[4, 4, 4, 4], [2, 4, 4, 3, 3]],
            17: [[2, 4, 4, 4, 3]],
            18: [[2, 4, 4, 4, 4]]}

        self.loss = False
        self.player_wind = 1
        self.round_wind = 1
        self.open_status = ['O'] * 5
        self.last_stone_flower = False
        self.last_stone_mid_straight = False

        self.base_characters = [character for character in characters if character[0] != 'f']

        # add the flower characters to the list
        self.flowers = [character for character in characters if character[0] == 'f']
        self.winning_configurations = None
        self.losing_configuration = None

    def update_open_status(self, status):
        self.open_status = status

    def update_loss(self):
        self.loss = not self.loss

    def update_player_wind(self, number):
        self.player_wind = number

    def update_round_wind(self, number):
        self.round_wind = number

    def get_possible_combinations(self, characters, combination_size):

        """
        This function calculates each possible combination given the remaining
        characters and the combination size. There are three possible combination
        size: 2, 3 and 4. Combination size 2 indicates a pair, size 4 a four-of-a
        -kind and 3 could be a three-of-a-kind or a straight.
        """

        if combination_size == 2:

            # select each possible pair that can be made using the remaining characters
            combinations = self.create_combination_unique_character(characters, 2, 2)

        elif combination_size == 4:
            # create list of possible four of kinds that can be made from remaining characters
            # in theory this output could contain combinations of characters
            # that are of a greater size than four but there are not more than
            # 4 of each character available in the game
            combinations = self.create_combination_unique_character(characters, 4)

        else:
            straights = []
            # calculate all possible three of a kinds with remaining characters
            three_of_a_kinds = self.create_combination_unique_character(characters, 3, 3)

            # generate each possible combination of unique characters
            # a straight always consist of three consecutive numbers thus
            # each character is different. when feeding unique characters to
            # the combinations function there are no duplicate combinations
            # created
            possible_straights = itertools.combinations(set(characters), 3)

            # add combination if the combination is a straight or a
            # three of a kind
            for combination in possible_straights:

                # convert from a tuple to a list such that the list can be sorted
                combination = list(combination)

                # make sure the combination is sorted from smallest to largest values
                combination.sort()

                # a combination is a straight if the numbers are an
                # uninterrupted consecutive list of three numbers
                # this is equal to the second value being equal to the
                # first value - 1 and the third value being equal to the
                # first value - 2
                if int(combination[0][1]) == int(combination[1][1]) - 1 == int(combination[2][1]) - 2:
                    straights += [combination]
            combinations = three_of_a_kinds + straights

        return combinations

    @staticmethod
    def remove_duplicate_configurations(configurations):

        """
        Configurations are lists of combinations which are lists of characters.
        A configuration is unique when at least there is at least one combination
        that differs is not present in the other configurations.
        """

        # check each configuration
        for configuration in configurations:

            # make a list of configurations without the current configuration
            other_configurations = configurations.copy()
            other_configurations.remove(configuration)

            # check configuration against each other configuration in list
            for other_configuration in other_configurations:

                # set value to determine if the configurations are different from each other
                different = False

                # check each combination in configuration
                for combination in configuration:

                    # if there is at least one combination not present in the other
                    # configuration then the configurations are different
                    if combination not in other_configuration:
                        different = True
                        break
                # if each combination is present in the other configuration then
                # the configurations are the same and one of these configurations can
                # be removed
                if not different:
                    configurations.remove(other_configuration)

        return configurations

    def get_number_configurations(self, characters, pattern):
        """
        hi
        """

        configurations = [[]]

        # identify possible combinations for each combination size in the pattern
        for combination_size in pattern:

            # create list of new configurations to store the new configurations
            # while still using the list of configurations
            new_configurations = []

            # get the partial configuration from the list of configurations
            # it is partial because not each necessary combination has been added
            for partial_configuration in configurations:

                # copy the list of characters to create a list of the characters
                # that still need to be grouped in combinations
                remaining_characters = characters.copy()

                # remove each character from each combination in the configuration
                for combination in partial_configuration:
                    for character in combination:
                        remaining_characters.remove(character)

                # get all valid configurations
                combinations = self.get_possible_combinations(remaining_characters,
                                                              combination_size)

                # if a combination has been found add new configuration(s) to the
                # list of new configurations
                if not combinations:
                    new_configurations += [partial_configuration + [combination]
                                           for combination in combinations]

            # after all configurations have been checked set refresh configurations
            # so that the next combination size can be checked
            configurations = new_configurations

        # remove the duplicate configurations
        configurations = self.remove_duplicate_configurations(configurations)
        return configurations

    def get_possible_configurations(self):

        """
        Get all possible combinations that can be made of the stones of a certain
        category. The stones of the other category are not number stones, thus
        they are processed differently. A straight is possible combination for
        number categories. A straight contains characters that are not the same.
        For the other category only combinations where the characters are the same
        are allowed. For a straight the category of the characters needs to be the
        same. For the other characters a character is always grouped together with
        characters that are the same thus there is only one configuration of
        other characters. Number character can be in a straight or a combination
        of the same characters. Therefore, a character can be present in many
        combinations, which can result in various possible configurations
        of the same characters.
        """

        categories = ['b', 'n', 'c', 'd', 'w']
        configurations = [[]]

        # calculate the possible configurations for each category
        for category in categories:

            # select all the characters belonging to the relevant category
            category_characters = [character for character in self.base_characters
                                   if character[0] == category]
            if category == 'd' or category == 'w':

                # calculate the possible combinations of the 'other' stones
                category_configurations = [self.create_combination_unique_character(category_characters)]

            else:

                category_configurations = []
                # given the number of characters there is a defined set of possible combinations
                # for each allowed combination the possible configurations are calculated
                for pattern in self.allowed_configuration_pattern[len(category_characters)]:
                    category_configurations += self.get_number_configurations(category_characters, pattern)

                # if no combinations are found return alternative list because else there
                # is nothing inside the list, which produces problems later on
                if not category_configurations:
                    category_configurations = [[]]

            # print(configurations, category_configurations)
            # add all configurations of each category together
            configurations = [partial_configuration + category_configuration
                              for category_configuration in category_configurations
                              for partial_configuration in configurations]

        # remove a-ll configurations that do not meet the requirement of a winning hand

        for configuration in configurations:
            if not self.check_win_status(configuration):
                configurations.remove(configuration)

        self.winning_configurations = configurations

    @staticmethod
    def create_combination_unique_character(characters, min_size=2, max_size=4):

        """
        Group all characters together that are the exact same. Thus, combinations of
        similar characters are made. This size of this combination should be larger
        than 'min_size'. The default is set to two because in general single
        characters do not carry any value, but pairs and so on do. It is important
        to note that there is only one combination possible for each unique
        character because all the characters that are the same are grouped in
        the same combination.
        """

        # get each unique character out of the given set
        unique_characters = list(set(characters))
        combinations = []

        # for each unique character the size of the possible combination is
        # calculated then checked and if sufficient the combination is added to
        # the list of final combinations
        for character in unique_characters:

            # calculate how many times the characters occurs in the list
            count_character = characters.count(character)

            # this count automatically equals the size of the combination
            # therefore this count has to be at least the minimal size of a
            # combination
            if count_character >= min_size:
                # add the valid combination to the list of final combinations
                # only add the max_size of numbers to the combinations
                combinations += [[character] * min(count_character, max_size)]

        return combinations

    @staticmethod
    def check_win_status(configuration):

        """
        For a configuration to belong to a winning hand, there need to be five
        combinations of which one and only one needs to be of size 2. A combination
        is by definition of size 2, 3 or 4. Thus, the other four combinations need
        to have a size of 3 or 4. This function calculates whether a configuration
        aligns with the requirements of a winning hand.
        """

        # calculate pattern of the configurations
        pattern = [len(combination) for combination in configuration]

        # check if pattern aligns with win requirements
        win_status = bool(len(pattern) == 5 and pattern.count(2) == 1)
        return win_status

    def calculate_base_points(self, configuration, loss=False):
        """
        Calculate the amount of base points based on the configurations.
        """

        points = {}
        # amount of base points awarded to a winning hand
        if not loss:
            index = len(points)
            points[index] = {}
            points[index]['points'] = 20
            points[index]['interpretation'] = 'Win bonus'

        # for each flower 4 points are awarded
        if len(self.flowers) > 0:
            index = len(points)
            points[index] = {}
            points[index]['points'] = len(self.flowers) * 4
            points[index]['interpretation'] = self.flowers

        types = []

        # check what the added value is of each of the combination
        for combination in configuration:

            # collect the information on the combination
            category, type_combination, status, state = combination

            # add 2 points for pairs dragon pairs of wind pairs of high status
            if type_combination == 'P' and (category == 'd'
                                            or (category == 'w'
                                                and status == 'H')):
                index = len(points)
                points[index] = {}
                points[index]['points'] = 2
                points[index]['interpretation'] = combination

            # add points of the for each three or four-of-a-kind
            elif type_combination == 'T' or type_combination == 'F':

                # add 8 base points for three-of-a-kinds and 8 for four-of-a-kinds
                point = 2 * (1 + 3 * (type_combination == 'F'))

                # multiply the base points by two if the combination is in the closed
                # state
                point *= (1 + (state == 'C'))

                # multiply the base points by two if the combination is of the high
                # status
                point *= (1 + (status == 'H'))
                index = len(points)
                points[index] = {}
                points[index]['points'] = point
                points[index]['interpretation'] = combination

            # collect the types of each combination in the configuration
            types += [type_combination]

        # if a winning hand contains four straights and a pair an extra 20 points
        # are awarded. As each winning hand contains a combination of type pair
        # if a winning hand contains 4 straights a similar result is obtained.
        if types.count('S') == 4 and not loss:
            index = len(points)
            points[index] = {}
            points[index]['points'] = 20
            points[index]['interpretation'] = 'Pianus'

        total_base_points = sum([item['points'] for item in points])
        return points, total_base_points

    def calculate_multiplier(self, configuration, loss):
        """
        Calculate the multiplier based on the configuration. A count of the amount
        of multipliers is measured.
        """

        multipliers = []

        # add 1 multipliers if each of the flowers is part of a player's hand
        if 'F1' in self.flowers and 'F2' in self.flowers and 'F3' in self.flowers and 'F4' in self.flowers:
            multipliers += ['All Flowers']

        # add 1 multiplier if each of the seasons is part of a players' hand
        if 'F5' in self.flowers and 'F6' in self.flowers and 'F7' in self.flowers and 'F8' in self.flowers:
            multipliers += ['All Seasons']

        # add 1 multiplier for each of the flowers or season belonging to player
        # are present in the hand
        if 'F' + str(self.player_wind) in self.flowers:
            multipliers.append('Player Flower')
        if 'F' + str(self.player_wind + 1) in self.flowers:
            multipliers.append('Player Season')

        categories = []
        types = []

        # check what multipliers can be obtained from each of the combination
        for combination in configuration:

            category, type_combination, status, _ = combination

            # for each four or three-of-a-kind of the dragon category or the high
            # status wind category a multiplier is added
            if type_combination != 'P' and category == 'd':
                multipliers.append('Dragon')

            if type_combination != 'P' and (category == 'W' and status == 'H'):
                multipliers.append('Player or Round Wind')

            # store the categories and types of each combination in the configuration
            categories += [category]
            types += [type_combination]

        # add three multipliers if all the combinations in a configuration are of
        # the same category and the configuration is a winning hand
        if len(set(categories)) == 1 and not loss:
            multipliers.append("All Character")

        # 1 multiplier is added if a winning hand contains only one or not any
        # number category
        elif not loss:

            # remove dragon and wind categories such that only the number categories
            # are left in the list
            categories = [category for category in categories
                          if category != 'd' and category != 'w']

            # add multiplier if there is one or not any number category
            if len(set(categories)) <= 1:
                multipliers.append("Character")

        # if the configuration does not contain any straight a multiplier is added
        if 'S' not in types and not loss:
            multipliers.append('All Pongs')

        return multipliers

    @staticmethod
    def get_type_combination(combination):
        """
        Get the type of the combination. A combination is either a pair, straight,
        three-of-a-kind or a four of a kind.
        """
        # if valid combination contains two characters it is a pair
        if len(combination) == 2:
            return 'P'

        # if a valid combination contains four character is a four-of-a-kind
        elif len(combination) == 4:
            return 'F'

        # if all characters of the combination are equal, and it contains three
        # characters it is a three-of-a-kind otherwise it is a straight
        elif len(set(combination)) == 1:
            return 'T'
        else:
            return 'S'

    def get_status_combination(self, combination):

        """
        Get value status of the combination. A combination has a high status if it
        is a dragon, the player wind, the round wind or character one or nine of
        the number categories.
        """

        # collect number and category of the first character of the combination
        # for non-straight combinations each character of the combination is the
        # same thus the first character describes the entire combination
        category = combination[0][0]

        number = int(combination[0][-1])

        # dragon combination are always of high status
        if category == 'd':
            return 'H'

        # wind combinations where the number is equal to the player of round wind
        # are of high status
        elif category == 'w' and (number == self.player_wind or number == self.round_wind):
            return 'H'

        # character one or nine of non-straight combinations of the number category
        # are of high status
        elif len(set(combination)) == 1 and (number == 1 or number == 9):
            return 'H'

        # otherwise, the combination has the low status
        else:
            return 'L'

    def reformat_configuration(self, configuration):

        """
        To easily analyze the combinations in a configuration the different
        combinations are coded. The code consists of four values:
            The first value is the category
            The second value is the type of combination:
                pair: two similar characters
                three-of-a-kind: three similar characters
                straight: three consecutively ascending number characters
                four-of-a-kind: four similar characters
            The third value is whether the characters are high or low. Dragons are
            always high characters. The player wind and round wind are also high
            characters. The ones and nines of the number characters are also high
            characters.
            The fourth value if the combination was closed or open
        """

        reformated_configuration = []
        # reformat each combination in the configuration
        for index, combination in enumerate(configuration):
            # fill the first value with the category of the combination
            reformated_combination = combination[0][0]

            # fill the second value with type of the combination
            reformated_combination += self.get_type_combination(combination)

            # fill the third value with the status of the combination
            reformated_combination += self.get_status_combination(combination)

            # fill the status with the state of the combination
            reformated_combination += self.open_status[index]

            # add reformated combination to the reformated configuration list
            reformated_configuration += [reformated_combination]

        return reformated_configuration

    def get_losing_configuration(self):

        self.losing_configuration = [self.create_combination_unique_character(self.base_characters)]

    def calculate_points_configuration(self, configuration, loss=False):

        # reformat the combinations of the configuration for easier calculation
        # of the points
        reformated_configuration = self.reformat_configuration(configuration)

        # calculate the base points given the configuration
        base_points, total_base_points = self.calculate_base_points(reformated_configuration, loss)

        # calculate the multiplier given the configuration
        multipliers = self.calculate_multiplier(reformated_configuration, loss)

        # if more than 3 multipliers are obtained the maximum value of 500 is
        # obtained if it belongs to a winning hand
        if len(multipliers) > 3 and not loss:
            final_points = 500

        # calculate the points by calculate by doubling the base points once
        # per added multiplier
        else:
            unrounded_points = total_base_points * 2 ** len(multipliers)

            # round up the points to the nearest multiple of 10
            final_points = (unrounded_points - 1) // 10 * 10 + 10

        return base_points, total_base_points, multipliers, final_points, configuration

    def calculate_points(self):

        """
        Calculate the maximum amount of points that can be obtained with the given
        characters. First calculate the possible configurations given the characters.
        Next calculate for each configuration what the score belongs to the given
        configuration. Select the configuration that has the highest score.
        """

        if self.winning_configurations is None:
            self.get_possible_configurations()

        if self.losing_configuration is None:
            self.get_losing_configuration()

        # the base characters are the characters that are not flowers
        final_info = None
        if not self.loss and self.winning_configurations != []:
            max_points = 0
            # calculate the amount of points for each configuration
            for configuration in self.winning_configurations:
                point_info = self.calculate_points_configuration(configuration)
                if point_info[3] > max_points:
                    final_info = point_info
        else:
            final_info = self.calculate_points_configuration(self.losing_configuration,
                                                             loss=True)

        return final_info
