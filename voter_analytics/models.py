from django.db import models
import traceback


# Create your models here.
class Voter(models.Model):
    '''
    Store/represent the data from one voter from Newton
    '''
    # identification
    last_name = models.TextField()
    first_name = models.TextField()
    dob = models.DateField()

    street_number = models.IntegerField()
    street_name = models.TextField()
    apartment_num = models.TextField()
    party_affiliation = models.TextField()
    zip_code = models.IntegerField()
    reg_date= models.DateField()
    party_affiliation = models.TextField()

    precinct =  models.TextField()
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()

    voter_score = models.IntegerField()

def load_data():
    '''Function to load data records from CSV file into Django model instances.'''

    Voter.objects.all().delete()
	
    filename = '/Users/meeramalhotra/Downloads/newton_voters.csv'
    f = open(filename)
    f.readline() # discard headers

    for line in f:
        fields = line.split(',')
       
        try:
            # create a new instance of Result object with this record from CSV
            voters = Voter(
                            last_name=fields[1],
                            first_name=fields[2],
                            street_number=fields[3],
                            street_name=fields[4],
                        
                            apartment_num = fields[5],
                            zip_code = fields[6],
                            dob = fields[7],
                            reg_date = fields[8],

                            party_affiliation = fields[9].replace(" ", ""),
                            precinct = fields[10],

                            v20state = bool_to_bool(fields[11]),
                            v21town = bool_to_bool(fields[12]),
                            v21primary = bool_to_bool(fields[13]),
                            v22general = bool_to_bool(fields[14]),
                            v23town = bool_to_bool(fields[15]),
                            
                            
                            voter_score = fields[16].strip()
                        )
        
            voters.save() # commit to database
            print(f'Created result: {voters}')
            print(f"Here are the: {fields}")
            
        except:
            print(traceback.format_exc())

            print(f"Skipped: {fields}")
    
    print(f'Done. Created {len(Voter.objects.all())} Results.')


def bool_to_bool(val):
    if val =="TRUE":
        return True
    else:
        return False
        