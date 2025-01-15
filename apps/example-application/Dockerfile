FROM fedora:39

RUN useradd -g root default && \
    dnf install -y python3.11 python3.11-devel librdkafka-devel gcc 

COPY --chown=default:0 --chmod=775 . /application/
WORKDIR /application

USER default
# Install with --no-deps as otherwise we get clashses, all deps have been included in requirements.txt
RUN python3.11 -m venv .venv && \
  source .venv/bin/activate && \
  pip install --no-deps -r requirements.txt && \
  chmod -R 775 .

CMD ["/bin/bash", "-c", "source .venv/bin/activate && python3 /application/ExampleApplication.py"]