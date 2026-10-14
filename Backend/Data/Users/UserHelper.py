import pandas as pd
import hashlib

class UserClass:

    def __init__(self, usr):
        self.displayname = usr["displayname"]
        self.sessionToken = usr["sessionToken"]
        self.uniqueId = usr["uniqueId"]
        self.mail = usr["mail"]
        self.passwordHash = usr["passwordHash"]
        

class UserHelper:

    def __init__(self, csv_path: str):
        self.csv_path = csv_path 

        # --------- Dataframes --------#

        dtype = {
            "uniqueId": str
        }

        self.Indexed_DFs = {
            "reg": pd.read_csv(self.csv_path, sep=',', dtype=dtype)
        }

        # --------- lookup_tables --------#
        self.lookup_tables = {
            "creds": {
                mail: pw_hash
                for mail, pw_hash in zip(self.Indexed_DFs["reg"]["mail"], self.Indexed_DFs["reg"]["passwordHash"])
            },

            "mail_session": {
                mail: session
                for mail, session in zip(self.Indexed_DFs["reg"]["mail"], self.Indexed_DFs["reg"]["sessionToken"])
            },
            "id_usr": {
                id: ind
                for ind, id in enumerate(self.Indexed_DFs["reg"]["uniqueId"])
            }
        }


    def GetUser(self, id: str)-> UserClass:
        '''
        Get a user via a unique id

        params:

        id=> the user unique id
        '''

        try:
            user = UserClass(self.Indexed_DFs["reg"].iloc[self.lookup_tables["id_usr"][id]])
            return user
        except KeyError:
            return None

    def CheckCredentials(self, mail: str, pw_hash: str)->int:
        '''
        Check if credentials are valid

        params:
        mail=> the user email ; 
        pw_hash=> the user hashed password to check if matching current hash

        return values:
        0=> incorrect pw ;
        1=> valid ;
        -1=> user doesn't exist/encountered error during lookup
        '''

        try:
            return 1 if self.lookup_tables["creds"][mail] == pw_hash else 0
        except KeyError:
            return -1

    def GetUserSession(self, mail: str)-> str:
        '''
        Get session via mail

        params:

        mail=> the user email ; 

        return values:

        json string=> the user session ; 

        -1=> the user is not in the lookup table
        '''

        try:
            return self.lookup_tables["mail_session"][mail]
        except KeyError:
            return None


UserHelperInst = UserHelper(r'Backend\Data\Users\Users.csv')
user = UserHelperInst.GetUser("0000001")
print(UserHelperInst.GetUserSession(user.mail))