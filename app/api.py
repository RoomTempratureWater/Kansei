from fastapi import FastAPI, Request, UploadFile, BackgroundTasks, File
from fastapi.templating import Jinja2Templates
import requests
from fastapi.middleware.cors import CORSMiddleware
import json
from .bgworker import bgworker
import os
import uvicorn
from typing import Annotated
import datetime
from .db import SUPAB
app = FastAPI()
supb = SUPAB()
supb.client_init()
templates = Jinja2Templates("app/templates")
import requests

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def name(request: Request):
    err = ""
    return templates.TemplateResponse('login.html', {"request": request, 'error': err})

@app.get('/login')
async def page2(request: Request):
    err = ''
    if 'error' in request.query_params:
        err = request.query_params['error']
    return templates.TemplateResponse('login.html', {"request": request, 'error': err})
@app.get('/me')
async def me(request:Request):
    user = {"name": "Jonathan"}
    return templates.TemplateResponse('me.html', {"request":request, "user": user})

@app.get('/getinfo/{token}')
async def getinfo(request:Request, token):
    res = requests.get("https://www.googleapis.com/oauth2/v3/userinfo",
                             headers={"Authorization":"Bearer"+token}) 
    dumped_res = res.text
    return dumped_res


@app.post('/upload')
async def uploadfile(request:Request, file: Annotated[UploadFile, File()], background_tasks: BackgroundTasks):
    data = await file.read()
    #print(request.headers, len(file))
    if "sub" in request.headers:
        #print(request.headers["sub"])
        background_tasks.add_task(generate_sumquest_json, mdfile=data, sub=request.headers["sub"], name=file.filename)
        return "<h4> {} uploaded successfully, wait for a few seconds and click show notes to see the uploaded file</h4>".format(file.filename)
    else:
        print("no")
        return "<h4>file upload failed </h4>"
    

def remove_file(path):
    os.remove(path)

def parse_data(data):
    format_str = "%Y-%m-%dT%H:%M:%S.%f%z"
    for note in data:
        time = datetime.datetime.strptime(note["created_at"], format_str)
        frmt = "%d-%m-%Y"
        note["created_at"] = time.strftime(frmt)
    return data
# BG task
async def generate_sumquest_json(mdfile, sub, name):
    md_str = mdfile.decode()
    dict_generator = bgworker(file=md_str)
    # print(dict_generator.mdfile)
    await dict_generator.get_doc_dict()
    file_json = json.dumps(dict_generator.doc, indent=2).encode('utf-8')
    nameforlink = supb.put_json(file_json, sub=sub)
    url = supb.get_json_url(nameforlink)
    data = {'Name': name, 'link_to_note':url, 'sub': sub}
    supb.insert(table='note', data_dict=data)
    print("done task") #<------ to comment
    

@app.get('/me/notes')
async def getnotes(request: Request):
    if "sub" in request.headers:
        data = supb.get_notes_of_user(sub=request.headers["sub"])
        data = data.data
        parsed_data = parse_data(data=data)
        return templates.TemplateResponse("data.html", {"request":request, "notes": parsed_data})
    else:
        return '<div>error</div>'

@app.get('/get-note/{noteid}')
async def note(request: Request, noteid):
    data = supb.get_note(id=noteid)
    data = data.data[0]
    link = data['link_to_note']
    name = data['Name']
    r = requests.get(link, 
                 headers={'Accept': 'application/json'})
    data_json = r.json()
    #print(data_json)
    return templates.TemplateResponse("note.html", {"request":request, "note": data_json, "name": name})  



# if __name__ == "__main__":
#    uvicorn.run("app:app", port=8000, reload=True)