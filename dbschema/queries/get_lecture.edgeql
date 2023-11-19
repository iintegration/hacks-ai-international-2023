select Lecture {
    id,
    status,
    filename
}
filter .id = <uuid>$id
limit 1