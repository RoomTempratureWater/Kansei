from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()
import os
import json
import uuid
import urllib.parse
class SUPAB():

    def __init__(self) -> None:
        self.client = None

    def client_init(self):
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        supabase: Client = create_client(url, key)
        self.client = supabase
    
    def insert(self, table, data_dict):
        if self.client == None:
            print("initialize client first")
            return False
        data = self.client.table(table).insert(data_dict).execute()
    
    def get_notes_of_user(self, sub):
        data = self.client.table("note").select("*").eq("sub", sub).order("created_at", desc=True).execute()
        return data

    def get_note(self, id):
        data = self.client.table("note").select("*").eq("id", id).execute()
        return data
    
    def put_json(self, json, sub):
        id = uuid.uuid1()
        id = urllib.parse.quote(str(id))
        full_path = '/{}/{}.json'.format(sub, id)
        data = self.client.storage.from_("MD_files").upload(full_path, json)
        return full_path
    
    def get_json_url(self, name):
        data = self.client.storage.from_("MD_files").get_public_url(name)
        #print(data)
        return data

'''url: str = os.environ.get("SUPABASE_TEST_URL")
key: str = os.environ.get("SUPABASE_TEST_KEY")
supabase: Client = create_client(url, key)
data = supabase.table("note").insert({"name":"Germany"}).execute()
assert len(data.data) > 0'''

if __name__ == "__main__":
    a = SUPAB()
    a.client_init()
    table = 'note'
    data = {'sub': '177212', 'Name':'Jonathannote', 'quiz':{'question1':'ans1'}, 'link_to_note':'www.xxx.com', 'summary_md':'jshadjwhajdhajwhd'}
    #a.insert(table=table, data_dict=data)
    #a.get_notes_of_user(3)
    k = json.dumps({'test2':'dict2'}, indent=2).encode('utf-8')
    a.put_json(k, '12323')

    