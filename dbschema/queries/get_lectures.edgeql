select Lecture {
    id,
    status,
    filename := .file.filename,
    error := .error
}