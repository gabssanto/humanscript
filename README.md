# humanscript

## Open Docker Python interpreter

Right now this is the only way to run HumanScript

```bash
docker build -t my-python-app .
docker run -it --rm --name my-running-app -v "$(pwd)":/app my-python-app
docker exec -it my-running-app /bin/bash
```

## Run HumanScript

```bash
dna examples/hello_world.dna
```

## Examples

### Hello world

```dna
tell "Hello world!"
```

### Function example

```dna
greetings as Function with
  name as String,
  age as Number do
  tell name
  tell age
end

call greetings "Gabriel", 24
```

## File extensions

- `.dna` - HumanScript source code
