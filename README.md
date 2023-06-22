# BOX

A simple CLI that helps you to create containers using podman.

### How to create a container setup:

Start creating a json file like this:

```json
[
    {
        "name": "hello-world",
        "image": "docker.io/library/hello-world:latest",
        "env": [
            ["TZ", "Etc/UTC"]
        ],
        "volumes": [
            ["/my_machine/dir", "/container/dir"]
        ],
        "ports": [
            [8080, 80, "tcp"]
        ]
    }
]
```

- This is an ilustractive example.

To create the container execute the box `create` command:

```shell
box create <YOUR_FILE>.json
```

- All others commands are used like this, `box command <YOUR_FILE>.json [CONTAINER]`, use the `help` command for more info.
