from fastapi import Depends, FastAPI, HTTPException, Query
import pickle
from modelsApi import Text,Base
from schema import TextSchema
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from preprocessing import read,plot_cm,process
import uvicorn
import configparser
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated

import logging

logging.basicConfig(filename='example.log',
                    encoding='utf-8',
                    format="%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(process)d >>> %(message)s",
                    datefmt="%Y-%m-%dT%H:%M:%SZ",
                    level=logging.DEBUG
)

'''logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')'''
Base.metadata.create_all(bind=engine)


app = FastAPI()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

config = configparser.ConfigParser()
config.read('config.ini')

@app.get('/')
def index():
    return {'message': 'text Detection ML API'}
output_api_predict = config['paths']['output_api_predict']

@app.post(output_api_predict)
async def predict_text_type(request:TextSchema,
                            db: Session = Depends(get_db),
                            input_file_model=config['paths']['input_file_model']
                            ):
    #load model
    with open(input_file_model, "rb") as f:
        model = pickle.load(f)

    #clean data 
    textin=request.text
    test_x=process(textin)
    # load data in list 
    test_x_list=[]
    test_x_list.append(test_x)

    #prediction
    #prediction= model.predict(test_x_list)
    prediction= model.predict_proba(test_x_list)[:,1]
    #sortie json
    is_spam= prediction[0] >= 0.5 
    if is_spam:
        valeur_out='spam'
        

    else: valeur_out='ham'
    # add to bdd 
    textresult=Text(text=textin,texte_clean=test_x,score_conf=round(prediction[0], 2),type_msg=valeur_out)
    db.add(textresult)
    db.commit()
    db.refresh(textresult)

    return textresult
        
@app.get(output_api_predict)
def get_output_api_predict(db: Session = Depends(get_db)) :
    bdd = db.query(Text)
    
    return bdd.all()
output_api_readtype=config['paths']['output_api_readtype']
@app.get(output_api_readtype)
def get_specific_type_predict(typepred=str,
                              db: Session = Depends(get_db)):
    if typepred in ['spam','ham']:
        
        bdd=db.query(Text).filter(Text.type_msg == typepred)
        return bdd.all()
    raise HTTPException(status_code=404, detail="Aucun type ne répond aux critères de recherche")
output_api_nbspam=config['paths']['output_api_nbspam']
@app.get(output_api_nbspam)
def get_nbspam(db: Session = Depends(get_db)):
        bdd=db.query(Text).filter(Text.type_msg == "spam")
        
        return {"nb_spam": bdd.count()}
  
if __name__ == '__main__':
    uvicorn.run("api:app", host='127.0.0.1', port=8000, reload=True)
