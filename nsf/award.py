"""
Extracts and stores information for an NSF award record.
"""
import datetime


class Award:
    def __init__(self, soup):
        self.soup = soup

        self.title = self.text('AwardTitle')
        self.id = self.text('AwardID')
        self.abstract = self.text('AbstractNarration')
        
        self.instruments = [t.text for t in soup.find_all('Value')]
        
        self.effective = self.date('AwardEffectiveDate')
        self.expires = self.date('AwardExpirationDate')
        self.first_amended = self.date('MinAmdLetterDate')
        self.last_amended = self.date('MaxAmdLetterDate')
        
        amount = self.text('AwardAmount')
        self.amount = int(amount) if amount else 0
        
        arra_amount = self.text('ARRAAmount')
        self.arra_amount = int(arra_amount) if arra_amount else 0
        
        directorate = soup.find('Directorate')
        directorate = directorate.find('LongName') if directorate else ''
        self.directorate = directorate.text if directorate else ''
        
        division = soup.find('Division')
        division = division.find('LongName') if division else ''
        self.division = division.text if division else ''
        
        self.pgm_elements = []
        for pgm in soup('ProgramElement'):
            code = pgm.find('Code')
            code = code.text if code else ''
            name = pgm.find('Text')
            name = name.text if name else ''
            self.pgm_elements.append({
                'code': code, 
                'name': name
            })

        self.pgm_references = []
        for pgm in soup('ProgramReference'):
            code = pgm.find('Code')
            code = code.text if code else ''
            name = pgm.find('Text')
            name = name.text if name else ''
            self.pgm_references.append({
                'code': code, 
                'name': name
            })
        
        self.institutions = []
        for tag in soup('Institution'):
            name = tag.find('Name')
            name = name.text if name else ''
            city = tag.find('CityName')
            city = city.text if city else ''
            state = tag.find('StateName')
            state = state.text if state else ''
            self.institutions.append({
                'name': name,
                'city': city,
                'state': state
            })

        self.investigators = []
        for tag in soup('Investigator'):
            email = tag.find('EmailAddress')
            email = email.text if email else ''
            first_name = tag.find('FirstName')
            first_name = first_name.text if first_name else ''
            last_name = tag.find('LastName')
            last_name = last_name.text if last_name else ''
            full_name = f'{first_name} {last_name}'
            start = tag.find('StartDate')
            start = start.text if start else ''
            end = tag.find('EndDate')
            end = end.text if end else ''
            role = tag.find('RoleCode')
            role = role.text if role else ''
            self.investigators.append({
                'name': full_name,
                'email': email,
                'start': start,
                'end': end,
                'role': role
            })

        self.program_officers = []
        for tag in soup('ProgramOfficer'):
            officer = tag.text.strip('\n') if tag else ''
            self.program_officers.append(officer)

    def flat_institutions(self):
        institutions = []
        for inst in self.institutions:
            flat_inst = f'{inst["name"]} - {inst["city"]}, {inst["state"]}'
            institutions.append(flat_inst)
        return '\n'.join(institutions)

    def flat_pgm_elements(self):
        pgm_elements = []
        for pgm in self.pgm_elements:
            flat_pgm = f'{pgm["code"]} : {pgm["name"]}'
            pgm_elements.append(flat_pgm)
        return '\n'.join(pgm_elements)

    def flat_pgm_references(self):
        pgm_references = []
        for pgm in self.pgm_references:
            flat_pgm = f'{pgm["code"]} : {pgm["name"]}'
            pgm_references.append(flat_pgm)
        return '\n'.join(pgm_references)

    def flat_investigators(self):
        investigators = []
        for i in self.investigators:
            flat_inv = f'{i["name"]}, {i["role"]}: {i["email"]}'
            investigators.append(flat_inv)
        return '\n'.join(investigators)

    def text(self, name):
        tag = self.soup.find(name)
        if tag:
            return tag.text.strip()
        else:
            return ''

    def date(self, name):
        text = self.text(name)
        if text:
            m, d, y = [int(p) for p in text.split('/')]
            return datetime.date(y, m, d)
        else:
            return ''

    def flatten(self):
        return {
            'title': self.title,
            'id': self.id,
            'abstract': self.abstract,
            'instruments': '\n'.join(self.instruments),
            'effective': self.effective,
            'expires': self.expires,
            'first_amended': self.first_amended,
            'amount': self.amount,
            'arra_amount': self.arra_amount,
            'directorate': self.directorate,
            'division': self.division,
            'pgm_elements': self.flat_pgm_elements(),
            'pgm_refs': self.flat_pgm_references(),
            'institutions': self.flat_institutions(),
            'investigators': self.flat_investigators(),
            'program_officers': '\n'.join(self.program_officers)
        }
    
    @classmethod
    def fieldnames(cls):
        return self.flatten().keys()
    
    @property
    def filename(self):
        return f'{self.id}.xml'
