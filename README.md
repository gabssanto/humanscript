# humanscript

## Open Docker Python interpreter

```bash
docker build -t my-python-app .
docker run -it --rm --name my-running-app -v "$(pwd)":/app my-python-app
docker exec -it my-running-app /bin/bash
```

## Run HumanScript

```bash
dna examples/hello_world.dna
```

## File extensions

- `.dna` - HumanScript source code
