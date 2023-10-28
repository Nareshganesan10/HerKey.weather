# Use the official Python image as the base image
FROM python:3.8

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the Python packages listed in requirements.txt
RUN pip install -r requirements.txt

# Copy the entire Django project into the container
COPY . /app/

# Expose the port on which your Django app will run (default is 8000)
EXPOSE 8000

# Start the Django development server
CMD ["python", "manage.py", "runserver"]