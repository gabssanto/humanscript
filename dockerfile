# Use an official Python runtime as a parent image
FROM python:latest

# Set the working directory in the container to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
# Uncomment the next line if you have a requirements.txt file
# RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable (optional)
ENV NAME World

# Run app.py when the container launches
# Uncomment the next line if you have an app.py file
# CMD ["python", "app.py"]

RUN echo 'alias dna="python3 interpreter.py"' >> ~/.bashrc

# Otherwise, just start a Bash shell
CMD ["/bin/bash"]
