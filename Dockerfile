FROM python

WORKDIR /

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "manage.py", "runserver"]