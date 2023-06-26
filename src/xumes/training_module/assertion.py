import numpy as np
from scipy.stats import ttest_1samp
from statsmodels.stats.proportion import proportions_ztest


def check_equal_values(sample, pop_mean):
    if all(value == pop_mean for value in sample):
        return True
    else:
        return False


def hypothesis_test(sample, pop_mean, alpha):
    equal_values = check_equal_values(sample, pop_mean)

    if equal_values:
        return None, None, None, None, False

    t_statistic, p_value_t = ttest_1samp(sample, pop_mean)

    count = sum([1 for value in sample if value == pop_mean])
    nobs = len(sample)
    _, p_value_prop = proportions_ztest(count, nobs, pop_mean)

    p_value_combined = min(p_value_t, p_value_prop) * 2

    if p_value_combined < alpha:
        significant_difference = True
    else:
        significant_difference = False

    return t_statistic, p_value_t, p_value_prop, p_value_combined, significant_difference


class AssertionStrategy:

    def __init__(self, alpha=0.01):
        self._alpha = alpha
        self._type = None

    def test(self, data) -> bool:
        if self._type is None:
            raise NotImplementedError("Assertion type is not defined")
        if len(data) == 0:
            raise ValueError("Data is empty")
        if not isinstance(data[0], self._type):
            raise TypeError("Data type is not equal to assertion type")

        return False


class AssertionEqual(AssertionStrategy):

    def __init__(self, value):
        super().__init__()
        self._value = value
        self._type = type(value)

    def test(self, data) -> bool:
        super().test(data)

        value = self._value
        if self._type == bool:
            data = np.array([1 if x else 0 for x in data])
        elif self._type != float and self._type != int:
            data = np.array([1 if x == self._value else 0 for x in data])
            value = 1

        t_statistic, p_value_t, p_value_prop, p_value_combined, significant_difference = hypothesis_test(data, value,
                                                                                                         self._alpha)

        if (self._type == int or self._type == float) and p_value_t:
            return p_value_t > self._alpha

        elif (self._type == bool or self._type == str) and p_value_combined:
            return p_value_combined > self._alpha

        return not significant_difference


class AssertionBetween(AssertionStrategy):

    def __init__(self, min_value, max_value):
        super().__init__()
        assert min_value < max_value
        assert type(min_value) == type(max_value)
        self._min_value = min_value
        self._max_value = max_value
        self._type = type(min_value)

    def test(self, data) -> bool:
        super().test(data)

        if self._type != float and self._type != int:
            data = np.array([1 if self._min_value <= x <= self._max_value else 0 for x in data])
            value = 1

            t_statistic, p_value_t, p_value_prop, p_value_combined, significant_difference = hypothesis_test(data,
                                                                                                             value,
                                                                                                             self._alpha)

            if p_value_combined:
                return p_value_combined > self._alpha

            return not significant_difference

        else:

            t_statistic_min, p_value_t_min, p_value_prop_min, p_value_combined_min, significant_difference_min = hypothesis_test(
                data, self._min_value,
                self._alpha)
            t_statistic_max, p_value_t_max, p_value_prop_max, p_value_combined_max, significant_difference_max = hypothesis_test(
                data,
                self._max_value,
                self._alpha)

            if t_statistic_max and t_statistic_min:
                return t_statistic_max < 0 < t_statistic_min
            else:
                return self._min_value <= np.mean(data) <= self._max_value


class AssertionLessThan(AssertionStrategy):

    def __init__(self, value):
        super().__init__()
        self._value = value
        self._type = type(value)

    def test(self, data) -> bool:
        super().test(data)

        if self._type != float and self._type != int:
            data = np.array([1 if x < self._value else 0 for x in data])
            value = 1

            t_statistic, p_value_t, p_value_prop, p_value_combined, significant_difference = hypothesis_test(data,
                                                                                                             value,
                                                                                                             self._alpha)

            if p_value_combined:
                return p_value_combined > self._alpha

            return not significant_difference

        else:
            t_statistic, p_value_t, p_value_prop, p_value_combined, significant_difference = hypothesis_test(data,
                                                                                                             self._value,
                                                                                                             self._alpha)
            if p_value_t:
                return p_value_t / 2 < self._alpha and t_statistic < 0
            elif p_value_prop:
                return p_value_prop / 2 < self._alpha and t_statistic < 0
            else:
                return np.mean(data) < self._value


class AssertionLessThanOrEqual(AssertionStrategy):

    def __init__(self, value):
        super().__init__()
        self._value = value
        self._type = type(value)

    def test(self, data) -> bool:
        super().test(data)

        if self._type != float and self._type != int:
            data = np.array([1 if x <= self._value else 0 for x in data])
            value = 1

            t_statistic, p_value_t, p_value_prop, p_value_combined, significant_difference = hypothesis_test(data,
                                                                                                             value,
                                                                                                             self._alpha)

            if p_value_combined:
                return p_value_combined >= self._alpha

            return not significant_difference

        else:
            t_statistic, p_value_t, p_value_prop, p_value_combined, significant_difference = hypothesis_test(data,
                                                                                                             self._value,
                                                                                                             self._alpha)
            if p_value_t:
                return p_value_t / 2 <= self._alpha and t_statistic < 0
            elif p_value_prop:
                return p_value_prop / 2 <= self._alpha and t_statistic < 0
            else:
                return np.mean(data) <= self._value


class AssertionGreaterThan(AssertionStrategy):

    def __init__(self, value):
        super().__init__()
        self._value = value
        self._type = type(value)

    def test(self, data) -> bool:
        super().test(data)

        if self._type != float and self._type != int:
            data = np.array([1 if x > self._value else 0 for x in data])
            value = 1

            t_statistic, p_value_t, p_value_prop, p_value_combined, significant_difference = hypothesis_test(data,
                                                                                                             value,
                                                                                                             self._alpha)

            if p_value_combined:
                return p_value_combined > self._alpha

            return not significant_difference

        else:
            t_statistic, p_value_t, p_value_prop, p_value_combined, significant_difference = hypothesis_test(data,
                                                                                                             self._value,
                                                                                                             self._alpha)
            if p_value_t:
                return p_value_t / 2 < self._alpha and t_statistic > 0
            elif p_value_prop:
                return p_value_prop / 2 < self._alpha and t_statistic > 0
            else:
                return np.mean(data) > self._value


class AssertionGreaterThanOrEqual(AssertionStrategy):

    def __init__(self, value):
        super().__init__()
        self._value = value
        self._type = type(value)

    def test(self, data) -> bool:
        super().test(data)

        if self._type != float and self._type != int:
            data = np.array([1 if x >= self._value else 0 for x in data])
            value = 1

            t_statistic, p_value_t, p_value_prop, p_value_combined, significant_difference = hypothesis_test(data,
                                                                                                             value,
                                                                                                             self._alpha)
            if p_value_combined:
                return p_value_combined > self._alpha

            return not significant_difference

        else:
            t_statistic, p_value_t, p_value_prop, p_value_combined, significant_difference = hypothesis_test(data,
                                                                                                             self._value,
                                                                                                             self._alpha)
            if p_value_t:
                return p_value_t / 2 <= self._alpha and t_statistic > 0
            elif p_value_prop:
                return p_value_prop / 2 <= self._alpha and t_statistic > 0
            else:
                return np.mean(data) >= self._value
