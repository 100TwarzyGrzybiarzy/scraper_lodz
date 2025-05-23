from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import xmltodict
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pozwala na żądania ze wszystkich źródeł (domen)
    allow_credentials=True,  # Pozwala na przesyłanie ciasteczek (jeśli są używane)
    allow_methods=["*"],  # Pozwala na wszystkie metody HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Pozwala na wszystkie nagłówki HTTP
)

def parse_xml_to_dict(xml_file_path):
    with open(xml_file_path, 'r', encoding="utf-8") as xml_file:
        xml_content = xml_file.read()
    return xmltodict.parse(xml_content)

@app.get("/drugs")
async def get_drugs_json():
    try:
        data_dict = parse_xml_to_dict("rejestr.xml")
        return data_dict
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="XML file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)