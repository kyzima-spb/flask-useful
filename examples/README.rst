.. code-block::

    docker run --rm -ti \
        --name flask_1 \
        -p 5000:5000 \
        -v $(pwd)/examples:/app \
        -v $(pwd):/python_packages \
        -e FLASK_APP=blueprints \
        -e FLASK_DEBUG=1 \
        kyzimaspb/flask

