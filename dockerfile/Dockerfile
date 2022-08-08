FROM python:3
RUN pip3 install requests
RUN mkdir fetching-ws
WORKDIR fetching-ws
COPY *.py ./
ENTRYPOINT ["python3"]
CMD ["fetching_github_pullrequest_details.py"]
