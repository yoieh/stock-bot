# Use the official Python base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt .

# Install TA-Lib C library dependencies
RUN apt-get update && \
    apt-get install -y build-essential libssl-dev libffi-dev python-dev && \
    wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xzvf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    rm -r ta-lib ta-lib-0.4.0-src.tar.gz

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the stock_bot.py script into the container
COPY stock_bot.py .

# Run the script when the container is launched
CMD ["python", "stock_bot.py"]
