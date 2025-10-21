# Dockerfile

# Start from an official, lightweight Python image. 
# Using a specific version is a best practice for reproducibility.
FROM python:3.9-slim

# Set the working directory inside the container.
# All subsequent commands (COPY, RUN, CMD) will be relative to this path.
WORKDIR /app

# --- Dependency Installation ---
# This is the key to efficient builds. By copying ONLY the requirements file first,
# Docker will cache this layer. It will only re-run the 'pip install' step
# if 'requirements.txt' itself changes. If you only change your app code,
# the build will be much faster because it uses the cached dependency layer.
COPY requirements.txt .

# Install the dependencies. '--no-cache-dir' keeps the image size smaller.
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt

# --- Application Code ---
# Now, copy the rest of your application files (main.py, model.pkl) into the container.
# If you change these files, Docker will only re-run from this step onward.
COPY . .

# --- Expose the Port ---
# Inform Docker that the container listens on port 80 at runtime.
# This is good practice for documentation.
EXPOSE 80

# --- The Run Command ---
# This is the command that will be executed when the container starts.
# We are starting the uvicorn server.
#  - "main:app": Tells uvicorn to look in the 'main.py' file for an object named 'app'.
#  - "--host", "0.0.0.0": This is CRITICAL. It tells the server to listen for requests
#    coming from OUTSIDE the container. If you used '127.0.0.1' (the default),
#    it would only be accessible from within the container itself.
#  - "--port", "80": The port to run on inside the container.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]