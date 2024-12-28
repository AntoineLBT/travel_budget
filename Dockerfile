# Step 1: Use an official Python runtime as the base image
FROM python:3.11-slim

# Step 2: Set environment variables
ENV PYTHONUNBUFFERED 1

# Step 3: Set the working directory inside the container
WORKDIR /app

# Step 4: Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the Django project into the container
COPY . /app/

# Step 6: Expose port 8000 (default for Django development server)
EXPOSE 8000

# Step 7: Command to run Django (replace with your preferred entrypoint)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
