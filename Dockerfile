FROM public.ecr.aws/lambda/python:3.12

# Copy requirements file
COPY pyproject.toml poetry.lock README.md ${LAMBDA_TASK_ROOT}/

# Install the specified packages
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Copy function code
COPY app/ ${LAMBDA_TASK_ROOT}/app/

# Copy Lambda handler
COPY lambda_handler.py ${LAMBDA_TASK_ROOT}/

# Set the CMD to your handler
CMD [ "lambda_handler.handler" ]
