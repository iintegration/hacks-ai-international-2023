select Lecture {
    id,
    status,
    filename := .file.filename,
    object_name := <str>(.file.id),
    text := .text,
    error := .error
}