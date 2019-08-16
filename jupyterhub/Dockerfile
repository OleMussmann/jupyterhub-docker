FROM jupyterhub/jupyterhub:1.0.0

COPY jupyterhub_config.py .
COPY css.html .

RUN wget https://raw.githubusercontent.com/jupyterhub/jupyterhub/1.0.0/examples/cull-idle/cull_idle_servers.py

RUN pip install \
    dockerspawner==0.11.1

# inject some css into page root template
RUN sed -i -e '/<body>/r css.html' /opt/conda/share/jupyterhub/templates/page.html && \
	rm css.html
