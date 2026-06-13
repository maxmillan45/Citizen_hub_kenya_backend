from enum import Enum

class CategoryEnum(str, Enum):
    ARREST = 'arrest'
    LAND = 'land'
    EMPLOYMENT = 'employment'
    HEALTH = 'health'
    EDUCATION = 'education'
    FAMILY = 'family'
    VOTING = 'voting'
    TECHNOLOGY = 'technology'

class EventCategoryEnum(str, Enum):
    TOWN_HALL = 'town_hall'
    PUBLIC_CONSULTATION = 'public_consultation'
    CIVIC_EDUCATION = 'civic_education'
    COMMUNITY_MEETING = 'community_meeting'

class LanguageEnum(str, Enum):
    ENGLISH = 'en'
    SWAHILI = 'sw'

class CrimeCategoryEnum(str, Enum):
    THEFT = 'theft'
    ASSAULT = 'assault'
    CORRUPTION = 'corruption'
    LAND_DISPUTE = 'land_dispute'
    OTHER = 'other'
