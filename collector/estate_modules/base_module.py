import logging


class RealEstate(object):
    """
    Base class for creating estate modules that collect data prom specific real estate projects. Inherited classes
    should override "estate_name" and "pretty_name". estate_name is intended for storage purposes, should be unique
    within spoofDog instance and contain only a-zA-Z0-9_ characters. pretty_name is intended for presentation pruposes
    and should be human readable identification of real estate project, can contain any fancy characters you wish.

    Constants "free_const", "reserved_const" and "sold_const" are used to define sepcific values that real eastate
    developers use to identify free, reserved and sold flat
    """

    estate_name = ''
    pretty_name = ''

    # Please dont override following constants. If desired, change them here for all subcasses to sue same definition
    free_const = 'F'
    reserved_const = 'R'
    sold_const = 'S'

    def __init__(self):
        """
        Subclasses that override this method must always call parents __init__ method to properly initialize data
        variable
        """
        self.data = {}
        self.logger = logging.getLogger("spoofDog.collector.{0}".format(self.estate_name))

    def get_data(self):
        """
        Subclasses of RealEstate must override this method with their own implementation that retrieves raw data about
        real estate project. This method should fill self.data with dictionary keys that represent specific apartments
        in project and values that indicate their availability. Values in self.data dictionary should conform to
        following schema:
        self.free_const - Free apartment
        self.reserved_const - Reserved apartment
        self.sold_const - Sold apartment
        """
        raise NotImplementedError
