## Documentation
You can see below the API reference of this module.

### `PostReceive(options)`
Creates a new `PostReceive` instance.

#### Params
- **Object** `options`: An object containing the following fields:
 - `cwd` (String): The working directory to start processing in
 - `logging` (Boolean): Output logs if `true`
 - `config` (Object): The `options.json` to use for the build process (see example)

### `PostReceive.process()`
Run the build process

### `PostReceive.log(message)`
Log a message if `this.logging`

#### Params
- **Anything** `message`: Message to log to console

### `PostReceive.load_options()`
Parse `this.options` to load host specific options

### `PostReceive.run_commands(commands)`
Run list of shell commands sequentially, handling errors

#### Params
- **Array** `commands`: List of commands to run

### `PostReceive.clear_dir()`
Empty the `copy_to` directory, excluding paths in ignore list

### `PostReceive.move_files()`
Copy processed files to `copy_to` directory, excluding paths in ignore list

### `PostReceive.error(message)`
Handle build error

#### Params
- **String** `message`: Error message to be logged and sent in build failed email

