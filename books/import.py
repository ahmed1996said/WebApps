import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    i=0
    reader = csv.reader(f)
    First_line=True
    for isbn,title,author,year in reader:
    	if First_line:
    		First_line=False
    		continue
    	db.execute("INSERT INTO books (isbn,title,author,year) VALUES (:isbn, :title, :author,:year)",
                    {"isbn": isbn, "title": title,"author":author ,"year": year})
    	i=i+1
    	print(f"added {i}/5000")
    	db.commit()

if __name__ == "__main__":
    main()