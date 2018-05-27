import requests
import os

class USDAQuickStats:

    def __init__(self):
        self.urlget = "http://quickstats.nass.usda.gov/api/api_GET/"
        self.urlgetcounts = "http://quickstats.nass.usda.gov" \
                            "/api/get_counts/"
        self.urlgetparams = "http://quickstats.nass.usda.gov" \
                            "/api/get_param_values/"
        self.getparams = {}
        self.getparams["key"] = os.environ["USDA_API_KEY"]
        self.getparams["source_desc"] = None
        self.getparams["group_desc"] = None
        self.getparams["commodity_desc"] = None
        self.getparams["state_alpha"] = None  
        self.getparams["freq_desc"] = None
        self.getparams["year"] = None
        self.getparams["format"] = "CSV"

    def get(self):
        """Get a requests.response containing the QuickStats data."""

        try:
            countparams = self.getparams.copy()
            countparams.pop("format")
            r = requests.get(self.urlgetcounts,countparams)
            j = r.json()
            self.row_count = int(j["count"])
            if self.row_count <= 50000:
                self.response = requests.get(self.urlget,self.getparams)
                print("Got " + str(self.row_count) + " records.")
            else:
                print("Query would return more than 50000 rows. Add"
                       " more query criteria to return fewer records.")
        except:
            raise
            print("Couldn't create the response.")

    def get_param_values(self,param):
        """Gets a list of valid values for a given parameter."""

        try:
            params = {}
            params["key"] = self.getparams["key"]
            params["param"] = param
            r = requests.get(self.urlgetparams,params)
            return r            
        except:
            raise
            print("Couldn't get the parameter values.") 

    def save_as(self,filepath):
        """Save the requests.response.content to a file."""
        
        try:
            r = self.response
            f = open(filepath,"wb") 
            f.write(r.content)
        except:
            print("Couldn't save the file.")
