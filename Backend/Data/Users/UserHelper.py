import pandas as pd

class UserHelper:

    def __init__(self, UsrDF: str):
        self.UsrDF = UsrDF # user data file but i am to lazy to write it fully each time

        # --------- Dataframes --------#

        dtype = {
            "uniqueId": str
        }

        self.IDFs = { # IDFs -> IndexedDataFrames
            "reg": pd.read_csv(self.UsrDF, sep=',', dtype=dtype),
            "id": pd.read_csv(self.UsrDF, sep=',', index_col="uniqueId", dtype=dtype)
        }

    def GetUser(self, id: str):

        usr = self.IDFs["id"].loc[id]
        return usr



UserHelperInst = UserHelper(r'Backend\Data\Users\Users.csv')
UserHelperInst.GetUser("0000001")