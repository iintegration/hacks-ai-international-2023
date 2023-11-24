select Lecture {
    id,
    status,
    filename := .file.filename,
    object_name := .file.object_name,
    text := .text,
    error := .error,
    timestamps := .timestamps
}
filter .id = <uuid>$id
limit 1