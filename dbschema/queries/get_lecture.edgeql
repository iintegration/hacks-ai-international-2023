select Lecture {
    id,
    status,
    filename := .file.filename,
    object_name := <str>(.file.id)
}
filter .id = <uuid>$id
limit 1