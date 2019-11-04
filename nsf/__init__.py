import pathlib

URL = 'https://www.nsf.gov/awardsearch/download'

# data paths
AWARD_DATA = pathlib.Path(__file__).parent / 'data' / 'awards'
KEYWORD_DATA = pathlib.Path(__file__).parent / 'data' / 'keywords'

# TODO: Add directorate abbreviations for easier querying.
DIRECTORATES = [
    'Directorate for Geosciences',
    'National Nanotechnology Coordinating Office',
    'Directorate for Engineering',
    'Directorate for Education & Human Resources',
    'Directorate for Social, Behavioral & Economic Sciences',
    'OFFICE OF THE DIRECTOR',
    'Directorate for Mathematical & Physical Sciences',
    'Directorate for Biological Sciences',
    'Office of Polar Programs',
    'National Coordination Office',
    'Office of Information & Resource Management',
    'Directorate for Computer & Information Science & Engineering',
    'Office of Budget, Finance & Award Management'
]
