# File Systems API

Pluggable storage backends for simulation I/O.

## FileSystem Protocol

::: idfkit.simulation.fs.FileSystem
    options:
      show_root_heading: false
      show_root_toc_entry: false
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

## AsyncFileSystem Protocol

::: idfkit.simulation.fs.AsyncFileSystem
    options:
      show_root_heading: false
      show_root_toc_entry: false
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
      show_root_heading: false
      show_root_toc_entry: false
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

## AsyncLocalFileSystem

::: idfkit.simulation.fs.AsyncLocalFileSystem
    options:
      show_root_heading: false
      show_root_toc_entry: false
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
      show_root_heading: false
      show_root_toc_entry: false
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

## AsyncS3FileSystem

::: idfkit.simulation.fs.AsyncS3FileSystem
    options:
      show_root_heading: false
      show_root_toc_entry: false
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
