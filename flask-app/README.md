# docker_flask_germ
An barebones setup for any docker deployed flask app with simple pytests.

## Mirroring to a new repo

To use this germ, make a mirror of it into a new github repo.

For a new repo named `new_repository`:

Create the `new_repository` on [Github](https://github.com/new).

```(Bash)
mkdir scratch-dir; cd scratch-dir
# move to a scratch dir

git clone --bare https://github.com/BBischof/docker_flask_germ.git
# Make a bare clone of the repository

cd docker_flask_germ.git
git push --mirror https://github.com/BBischof/new_repository.git
# Mirror-push to the new repository

cd ..
rm -rf docker_flask_germ.git
# Remove our temporary local repository
```

## What is contained in this germ

The simple flask app(mysteriously named `flask_app.py`) has two routes
- `/hello`
- `/get_webpage`

The docker package uses `pip_requirements` for dependency management. Note the dockerfile needs the name of the app to run on up. The app is on the `web` service, configured to `port 5000`.

To build the container:

`docker-compose build`

And then to run use either,

`docker-compose up`

or, if you only want to start web services,

`docker-compose web up`.

With the app started\
`curl -X GET localhost:5000/hello`.

## Tests

Using pytest with monkeypatch for mocking.

There are two basic tests included in the germ. The second shows an example of the mocking.

To run tests,

`docker-compose run web pytest tests/`

Or a specific testfile,

`docker-compose run web pytest tests/test_app.py`

## License

This has MIT because nothing here is original or propreitary. This is just meant to make things easier for me/people.
