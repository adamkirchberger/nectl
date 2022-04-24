FROM python:3-slim as build

# Create venv
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install nectl package
COPY dist/*.whl /tmp
RUN pip install /tmp/*.whl

FROM python:3-slim

# Copy venv from build step
COPY --from=build /venv /venv
ENV PATH="/venv/bin:$PATH"

# Set working directory
WORKDIR /kit
VOLUME /kit

CMD ["bash"]
