# File Systems API

Pluggable storage backends for simulation I/O.

## FileSystem Protocol

::: idfkit.simulation.fs.FileSystem
    options:
      show_root_heading: true
      show_source: true
      members:
        - read_bytes
        - write_bytes
        - read_text
        - write_text
        - exists
        - makedirs
        - copy
        - glob
        - remove

## LocalFileSystem

::: idfkit.simulation.fs.LocalFileSystem
    options:
      show_root_heading: true
      show_source: true
      members:
        - read_bytes
        - write_bytes
        - read_text
        - write_text
        - exists
        - makedirs
        - copy
        - glob
        - remove

## S3FileSystem

::: idfkit.simulation.fs.S3FileSystem
    options:
      show_root_heading: true
      show_source: true
      members:
        - read_bytes
        - write_bytes
        - read_text
        - write_text
        - exists
        - makedirs
        - copy
        - glob
        - remove
