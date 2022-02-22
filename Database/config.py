import os

#from dotenv import load_dotenv

#load_dotenv()

db_url=(f"postgresql://nish:pXm8eBtg1IbW7TME@free-tier4.aws-us-west-2.cockroachlabs."
+f"cloud:26257/defaultdb?sslmode=verify-full&sslrootcert=$env:appdata\.postgresql\root.crt&options=--cluster%3Dpebbles-prod1-2069")

class Config(object):
    SQLALCHEMY_DATABASE_URI = db_url
    # when backend is elasticsearch, MSEARCH_INDEX_NAME is unused
    # flask-msearch will use table name as elasticsearch index name unless set __msearch_index__
