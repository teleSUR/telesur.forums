"""
Tomado de collective.contacts
"""
from zope.interface import implements, implementer, alsoProvides, Interface
from zope.schema.interfaces import IVocabulary, IVocabularyFactory
from zope.component import _api as zapi
from os import path

from zope.schema import vocabulary, Iterable

from iso3166 import CountriesStatesParser

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('telesur.forums')


class ICountriesStates(Interface):
    countries = Iterable(
        title = _(u"countries"),
        description=_(u"A list of countries")
        )
    states = Iterable(
        title = _(u"states"),
        description=_(u"A list of states")
        )


class TitledVocabulary(vocabulary.SimpleVocabulary):
    def fromTitles(cls, items, *interfaces):
        """Construct a vocabulary from a list of (value,title) pairs.

        The order of the items is preserved as the order of the terms
        in the vocabulary.  Terms are created by calling the class
        method createTerm() with the pair (value, title).

        One or more interfaces may also be provided so that alternate
        widgets may be bound without subclassing.
        """
        terms = [cls.createTerm(value,value,title) for (value,title) in items]
        return cls(terms, *interfaces)
    fromTitles = classmethod(fromTitles)

class CountriesStatesFromFile(object):
    """Countries utility that reads data from a file
    """
    implements(ICountriesStates)

    _no_value = [('--',_(u'(no value)'))]

    def __init__(self):
        iso3166_path = path.join(path.dirname(__file__), 'iso3166')
        self.csparser = CountriesStatesParser(iso3166_path)
        self.csparser.parse()
        self.loaded_countries = []

    def special_values(self):
        return [self._no_values[0]]
    special_values = property(special_values)

    def countries(self):
        #if self.loaded_countries:
        #    return self.loaded_countries
        names =  self.csparser.getCountriesNameOrdered()
        res = []
        for n in names:
            if len(n[1]) < 18:
                res.append( n )
            elif ',' in n:
                res.append( ( n[0], n[1].split(',')[0] ) )
            else:
                #This may show the countries wrongly abbreviated (in fact i am
                #almost sure it will, but is better than not showing them at all
                res.append( ( n[0], n[1][:18] ) )

        # need to pick this up some list of strings property in the admin interface
        def sorter( x, y, order=[]):
            if x[1] in order and y[1] in order:
                return cmp( order.index(x[1]), order.index(y[1]) )
            if x[1] in order:
                return -1
            if y[1] in order:
                return 1
            return cmp( x[1], y[1] )

        res.sort( sorter )
        res = self._no_value + res
        self.loaded_countries = res
        return res

    countries = property(countries)

    def states(self, country=None):
        if country is None:
            states = self.allStates()
        else:
            states = self._no_value + self.csparser.getStatesOf(country)
        return states

    def allStates(self):
        return self._no_value + self.csparser.getStatesOfAllCountries()

    def allStateValues(self):
        all_states = self.csparser.getStatesOfAllCountries()
        return self._no_value + all_states

@implementer(IVocabulary)
def Countries( context ):
    utility = zapi.getUtility(ICountriesStates)
    return TitledVocabulary.fromTitles(utility.countries)
alsoProvides(Countries, IVocabularyFactory)

@implementer(IVocabulary)
def States( context ):
    utility = zapi.getUtility(ICountriesStates)
    return TitledVocabulary.fromTitles(utility.allStateValues())
alsoProvides(States, IVocabularyFactory)
