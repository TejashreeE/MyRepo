FROM python
ADD . /app
COPY . .
WORKDIR /app
RUN pip3 install --no-cache-dir -r requirements.txt
