FROM python:3.8.9

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY ./packages.txt /app/packages.txt

RUN apt-get update && \
    xargs -r -a /app/packages.txt apt-get install -y && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Install Java Development Kit (JDK)
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g apk-mitm

# User
RUN useradd -m -u 1000 user
USER user
ENV HOME /home/user
ENV PATH $HOME/.local/bin:$PATH

WORKDIR $HOME
RUN mkdir app
WORKDIR $HOME/app
COPY . $HOME/app

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.headless", "true", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false", "--server.fileWatcherType", "none"]
