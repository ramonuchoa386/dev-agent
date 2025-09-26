FROM us-central1-docker.pkg.dev/vtal-sandbox-mystic/smartcode-ai/dev.agent-base:latest

COPY . .

RUN touch /app/logs/github_agent_$(date +%Y%m%d).log

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]