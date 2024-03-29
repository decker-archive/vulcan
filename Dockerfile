FROM python:3.10.4-alpine

# Used because of cchardet requiring GCC to work.
RUN apk add --no-cache build-base libffi-dev

WORKDIR /

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 443

CMD [ "gunicorn", "-w 9", "-k uvicorn.workers.UvicornWorker", "-b 0.0.0.0:443", "--certfile=real.crt", "--keyfile=real.key", "main:app" ]