# -*- coding: utf-8 -*-


def justified(price):
    """
    Return the given price, as str, with zero justified cents.

    :param price: the price to justify
    :type price: float
    :return: the given price, for which the cents are justified with zeros
    :rtype: str
    """
    _s = str(round(price, 2)).split('.')
    _s[-1] = _s[-1].ljust(2, '0')
    return '.'.join(_s)
