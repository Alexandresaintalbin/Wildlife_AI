# Set the base image to use for the container
FROM python:3.9

# Set the working directory for the container
WORKDIR /app

# Copy the requirements file and install the necessary packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files into the container
COPY . .

# Expose the port that the Django server will be running on
EXPOSE 8000

# Run the Django server when the container starts
CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]