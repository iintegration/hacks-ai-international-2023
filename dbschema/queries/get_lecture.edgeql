select Lecture {
    id,
    status,
    filename := .file.filename,
    object_name := .file.object_name,
    text := .text,
    error := .error,
    timestamps := .timestamps,
    terms := .terms { term, definition, start_timestamp, end_timestamp }
}
filter .id = <uuid>$id
limit 1